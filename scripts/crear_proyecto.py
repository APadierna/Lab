#!/usr/bin/env python3
"""
Crea un proyecto Vivado a partir de los ficheros fuente del repositorio.

Uso:
    python scripts/crear_proyecto.py
    scripts/crear_proyecto.bat          (Windows)
"""

import configparser
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT        = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
CONFIG_FILE = ROOT / "config.ini"
TCL_TMPL    = SCRIPTS_DIR / "plantilla_proyecto.tcl"
VIVADO_DIR  = ROOT / "vivado"


# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

def leer_config() -> configparser.ConfigParser:
    if not CONFIG_FILE.exists():
        sys.exit(f"[ERROR] No se encuentra config.ini en {ROOT}")
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_FILE, encoding="utf-8")
    return cfg


# ---------------------------------------------------------------------------
# Localización de Vivado
# ---------------------------------------------------------------------------

def _candidatos_vivado():
    """Genera rutas candidatas al ejecutable de Vivado en orden de prioridad."""
    nombres = ("vivado.bat", "vivado")

    # Variable de entorno XILINX_VIVADO=/ruta/Vivado/<version>
    env = os.environ.get("XILINX_VIVADO", "")
    if env:
        for n in nombres:
            yield Path(env) / "bin" / n

    # En el PATH
    for n in nombres:
        encontrado = shutil.which(n)
        if encontrado:
            yield Path(encontrado)

    # Búsqueda en rutas habituales de Windows
    for base in [Path("C:/Xilinx/Vivado"), Path("C:/Xilinx")]:
        if base.exists():
            for carpeta in sorted(base.iterdir(), reverse=True):
                for n in nombres:
                    yield carpeta / "bin" / n


def encontrar_vivado(exe_cfg: str) -> str | None:
    # Ruta explícita en config.ini
    if exe_cfg:
        p = Path(exe_cfg)
        if p.exists():
            return str(p)
        print(f"[AVISO] Ejecutable en config.ini no encontrado: {exe_cfg}")

    for candidato in _candidatos_vivado():
        if candidato.exists():
            return str(candidato)

    return None


# ---------------------------------------------------------------------------
# Generación del script TCL
# ---------------------------------------------------------------------------

def generar_tcl(nombre: str, top: str, parte: str) -> Path:
    VIVADO_DIR.mkdir(exist_ok=True)
    tcl = (TCL_TMPL.read_text(encoding="utf-8")
           .replace("@@ROOT_DIR@@",  str(ROOT).replace("\\", "/"))
           .replace("@@PROYECTO@@",  nombre)
           .replace("@@TOP@@",       top)
           .replace("@@PARTE@@",     parte))
    destino = VIVADO_DIR / "crear_proyecto.tcl"
    destino.write_text(tcl, encoding="utf-8")
    return destino


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    cfg     = leer_config()
    nombre  = cfg["proyecto"]["nombre"]
    top     = cfg["proyecto"]["modulo_top"]
    parte   = cfg["dispositivo"]["parte"]
    exe_cfg = cfg.get("vivado", "ejecutable", fallback="").strip()

    print(f"\n  Proyecto : {nombre}")
    print(f"  Top      : {top}")
    print(f"  Parte    : {parte}")

    vivado = encontrar_vivado(exe_cfg)
    if not vivado:
        sys.exit(
            "\n[ERROR] No se encontró Vivado.\n"
            "  Soluciones:\n"
            "  1. Añadir Vivado al PATH del sistema\n"
            "  2. Definir la variable XILINX_VIVADO apuntando a la instalación\n"
            "  3. Poner la ruta completa en config.ini bajo  ejecutable ="
        )
    print(f"  Vivado   : {vivado}\n")

    dir_proyecto = VIVADO_DIR / nombre
    if dir_proyecto.exists():
        resp = input(f"[AVISO] Ya existe '{dir_proyecto.name}'. ¿Sobreescribir? [s/N] ")
        if resp.strip().lower() != "s":
            print("Cancelado.")
            sys.exit(0)
        shutil.rmtree(dir_proyecto)

    tcl_path = generar_tcl(nombre, top, parte)
    print(f"[+] Script TCL generado: {tcl_path.relative_to(ROOT)}")
    print("[+] Ejecutando Vivado en modo batch...\n")

    resultado = subprocess.run(
        [vivado, "-mode", "batch", "-source", str(tcl_path)],
        cwd=ROOT,
    )

    if resultado.returncode == 0:
        xpr = dir_proyecto / f"{nombre}.xpr"
        print(f"\n[OK] Proyecto creado en vivado/{nombre}/")
        print(f"     Para abrirlo: vivado \"{xpr}\"\n")
    else:
        sys.exit(
            f"\n[ERROR] Vivado terminó con código {resultado.returncode}.\n"
            f"        Revisa vivado/vivado.log para más detalles."
        )


if __name__ == "__main__":
    main()
