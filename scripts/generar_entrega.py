#!/usr/bin/env python3
"""
Genera el zip de entrega del laboratorio.

Pasos:
  1. Verifica (y configura si falta) la identidad Git del alumno
  2. Commitea todos los cambios pendientes en src/, sim/ y config.ini
  3. Empaqueta el repositorio con git archive → <proyecto>_<alumno>_<fecha>.zip
"""

import configparser
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT        = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT / "config.ini"


# ---------------------------------------------------------------------------
# Utilidad git
# ---------------------------------------------------------------------------

def git(*args):
    return subprocess.run(
        ["git", *args],
        capture_output=True, text=True, cwd=ROOT,
    )


# ---------------------------------------------------------------------------
# 1 · Identidad
# ---------------------------------------------------------------------------

def _get(key):
    r = git("config", key)
    return r.stdout.strip() if r.returncode == 0 else ""


def verificar_identidad() -> str:
    """Devuelve user.name; guía al alumno si no está configurado."""
    name  = _get("user.name")
    email = _get("user.email")

    if name and email:
        print(f"  Nombre : {name}")
        print(f"  Email  : {email}")
        return name

    print("  Git necesita tu nombre y email para identificar la entrega.")
    print("  Solo se configura una vez (vale para todos tus repositorios).\n")

    if not name:
        while True:
            name = input("  Nombre completo    : ").strip()
            if name:
                break
            print("  El nombre no puede estar vacío.")
        subprocess.run(["git", "config", "--global", "user.name", name], cwd=ROOT)

    if not email:
        while True:
            email = input("  Email institucional: ").strip()
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                break
            print("  Introduce un email válido (p. ej. alumno@universidad.es).")
        subprocess.run(["git", "config", "--global", "user.email", email], cwd=ROOT)

    print(f"\n  Configurado: {name} <{email}>")
    return name


# ---------------------------------------------------------------------------
# 2 · Commit automático
# ---------------------------------------------------------------------------

def commitear_cambios(nombre_proyecto: str):
    status = git("status", "--porcelain")
    if not status.stdout.strip():
        print("  Sin cambios pendientes — el árbol de trabajo está limpio.")
        return

    print("  Cambios pendientes:")
    for linea in status.stdout.strip().splitlines():
        print(f"    {linea}")
    print()

    git("add", ".")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    mensaje   = f"Entrega: {nombre_proyecto} ({timestamp})"
    r = git("commit", "-m", mensaje)

    if r.returncode == 0:
        print(f"  Commit creado: \"{mensaje}\"")
    else:
        print(f"[ERROR] No se pudo hacer commit:\n{r.stderr}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# 3 · Zip con git archive
# ---------------------------------------------------------------------------

def _sanitizar(texto: str) -> str:
    """Convierte un nombre en un slug válido para nombre de fichero."""
    for orig, repl in [(" ", "_"),
                       ("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),
                       ("à","a"),("è","e"),("ì","i"),("ò","o"),("ù","u"),
                       ("ñ","n"),("ü","u"),("ç","c")]:
        texto = texto.lower().replace(orig, repl)
    return re.sub(r"[^a-z0-9_]", "", texto)


def generar_zip(nombre_proyecto: str, nombre_alumno: str):
    # Comprobar que HEAD existe (al menos un commit)
    if git("rev-parse", "--verify", "HEAD").returncode != 0:
        print("[ERROR] No existe ningún commit en el repositorio.")
        sys.exit(1)

    fecha      = datetime.now().strftime("%Y%m%d_%H%M")
    slug       = _sanitizar(nombre_alumno)
    nombre_zip = f"{nombre_proyecto}_{slug}_{fecha}.zip"
    dir_salida = ROOT / "entregas"
    dir_salida.mkdir(exist_ok=True)
    destino    = dir_salida / nombre_zip

    r = git("archive", "--format=zip", f"--output={destino}", "HEAD")
    if r.returncode == 0:
        size_kb = destino.stat().st_size // 1024
        print(f"  Fichero : {nombre_zip}  ({size_kb} KB)")
        print(f"  Ruta    : {destino}")
    else:
        print(f"[ERROR] git archive falló:\n{r.stderr}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not CONFIG_FILE.exists():
        sys.exit(f"[ERROR] No se encuentra config.ini en {ROOT}")

    cfg    = configparser.ConfigParser()
    cfg.read(CONFIG_FILE, encoding="utf-8")
    nombre = cfg["proyecto"]["nombre"]

    print(f"\n=== Entrega: {nombre} ===\n")

    print("[1/3] Verificando identidad Git...")
    nombre_alumno = verificar_identidad()

    print("\n[2/3] Commiteando cambios pendientes...")
    commitear_cambios(nombre)

    print("\n[3/3] Generando zip...")
    generar_zip(nombre, nombre_alumno)

    print("\n[OK] Entrega lista. Sube el zip al campus virtual.\n")


if __name__ == "__main__":
    main()
