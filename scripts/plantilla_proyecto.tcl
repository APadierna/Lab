# Generado automáticamente por crear_proyecto.py — no editar manualmente.

set root_dir "@@ROOT_DIR@@"
set nombre   "@@PROYECTO@@"
set top      "@@TOP@@"
set parte    "@@PARTE@@"

set dir_proyecto [file join $root_dir vivado $nombre]

# ----- Crear proyecto -----
create_project $nombre $dir_proyecto -part $parte

# ----- Ficheros HDL -----
set hdl_files {}
foreach patron [list \
    [file join $root_dir src hdl *.vhd] \
    [file join $root_dir src hdl *.v]   \
    [file join $root_dir src hdl *.sv]  \
] {
    foreach f [glob -nocomplain $patron] {
        lappend hdl_files $f
    }
}

if {[llength $hdl_files] > 0} {
    add_files -norecurse $hdl_files
    update_compile_order -fileset sources_1
    puts "\[info\] Ficheros HDL añadidos: [llength $hdl_files]"
} else {
    puts "\[aviso\] No se encontraron ficheros en src/hdl/"
}

# ----- Módulo top -----
set_property top $top [current_fileset]

# ----- Restricciones (XDC) -----
set xdc_files {}
foreach f [glob -nocomplain [file join $root_dir src constraints *.xdc]] {
    lappend xdc_files $f
}
if {[llength $xdc_files] > 0} {
    add_files -fileset constrs_1 -norecurse $xdc_files
    puts "\[info\] Restricciones añadidas: [llength $xdc_files]"
}

# ----- Ficheros de simulación -----
set sim_files {}
foreach patron [list \
    [file join $root_dir sim *.vhd] \
    [file join $root_dir sim *.v]   \
    [file join $root_dir sim *.sv]  \
] {
    foreach f [glob -nocomplain $patron] {
        lappend sim_files $f
    }
}
if {[llength $sim_files] > 0} {
    add_files -fileset sim_1 -norecurse $sim_files
    puts "\[info\] Ficheros de simulación añadidos: [llength $sim_files]"
}

puts "\n=== Proyecto '$nombre' creado correctamente ==="
puts "=== Abrir con: vivado [file join $dir_proyecto ${nombre}.xpr] ===\n"
