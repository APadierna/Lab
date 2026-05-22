# Plantilla de Proyecto Vivado — Laboratorio de Electrónica Digital

## Estructura del repositorio

```
.
├── config.ini              ← Nombre del proyecto, módulo top, dispositivo
├── scripts/
│   ├── crear_proyecto.py   ← Script principal (Python 3)
│   ├── crear_proyecto.bat  ← Acceso directo para Windows
│   └── plantilla_proyecto.tcl
├── src/
│   ├── hdl/                ← Ficheros VHDL (.vhd) — aquí va tu diseño
│   └── constraints/        ← Ficheros de restricciones (.xdc)
├── sim/                    ← Testbenches y ficheros de simulación
├── vivado/                 ← Directorio del proyecto Vivado (NO subir a Git)
└── .gitignore
```

## Requisitos

- Python 3.8 o superior
- Vivado (cualquier versión 2020+)

## Primeros pasos (alumno)

### 1. Configura el proyecto

Edita `config.ini` y cambia al menos el nombre del proyecto:

```ini
[proyecto]
nombre     = mi_practica1
modulo_top = top
```

### 2. Crea el proyecto Vivado

**Opción A — doble clic:**
Ejecuta `scripts/crear_proyecto.bat`

**Opción B — terminal:**
```
python scripts/crear_proyecto.py
```

El script detecta Vivado automáticamente. Si no lo encuentra, añade la ruta en `config.ini`:
```ini
[vivado]
ejecutable = C:/Xilinx/Vivado/2024.1/bin/vivado.bat
```

### 3. Abre el proyecto

El script imprime la ruta al final. También puedes abrirlo desde Vivado:
```
File → Open Project → vivado/<nombre>/<nombre>.xpr
```

## Flujo de trabajo

1. **Edita tus ficheros VHDL** en `src/hdl/` directamente (no en la interfaz de Vivado).  
   Vivado los referencia en su lugar — no crea copias.

2. **Añade más ficheros:** crea el `.vhd` en `src/hdl/` y luego en Vivado:  
   `Project Manager → Add Sources → Add or create design sources`

3. **Restricciones:** el fichero `src/constraints/basys3.xdc` ya está incluido.  
   Descomenta solo los puertos que uses.

4. **Simula** poniendo los testbenches en `sim/`.

## Qué subir a Git

| Subir (commit) | No subir (ignorado) |
|---|---|
| `src/hdl/*.vhd` | `vivado/` (directorio entero) |
| `src/constraints/*.xdc` | `*.bit`, `*.bin` |
| `sim/*.vhd` | `*.jou`, `*.log` |
| `config.ini` | `.Xil/` |
| `scripts/` | |

Cualquier compañero (o el profesor) puede recrear el proyecto Vivado en su máquina con:
```
python scripts/crear_proyecto.py
```

## Entrega

Ejecuta el script de entrega:

**Opción A — doble clic:**
`scripts/generar_entrega.bat`

**Opción B — terminal:**
```
python scripts/generar_entrega.py
```

El script hace tres cosas automáticamente:

1. **Verifica tu identidad Git.** La primera vez te pedirá nombre y email (se guarda para todos tus repositorios).
2. **Commitea todos los cambios pendientes** en `src/`, `sim/` y `config.ini`.
3. **Genera el zip** con nombre `<proyecto>_<tu_nombre>_<fecha>.zip` en la carpeta `entregas/`.

Sube ese zip al campus virtual.
