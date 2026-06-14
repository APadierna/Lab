# Generado automáticamente por crear_proyecto.py — no editar manualmente.

set root_dir "@@ROOT_DIR@@"
set nombre   "@@PROYECTO@@"
set top      "@@TOP@@"
set parte    "@@PARTE@@"

set dir_proyecto [file join $root_dir vivado $nombre]

# ----- Crear proyecto -----
create_project $nombre $dir_proyecto -part $parte

# ----- Utilidad: búsqueda recursiva de ficheros -----
proc find_files {dir extensiones} {
    set resultado {}
    foreach ext $extensiones {
        foreach f [glob -nocomplain [file join $dir $ext]] {
            lappend resultado $f
        }
    }
    foreach subdir [glob -nocomplain -type d [file join $dir *]] {
        lappend resultado {*}[find_files $subdir $extensiones]
    }
    return $resultado
}

# ----- Ficheros HDL -----
set hdl_files [find_files [file join $root_dir src hdl] {*.vhd *.v *.sv}]

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
set xdc_files [find_files [file join $root_dir src constraints] {*.xdc}]
if {[llength $xdc_files] > 0} {
    add_files -fileset constrs_1 -norecurse $xdc_files
    puts "\[info\] Restricciones añadidas: [llength $xdc_files]"
}

# ----- Ficheros de simulación -----
set sim_files [find_files [file join $root_dir sim] {*.vhd *.v *.sv}]
if {[llength $sim_files] > 0} {
    add_files -fileset sim_1 -norecurse $sim_files
    puts "\[info\] Ficheros de simulación añadidos: [llength $sim_files]"
}

puts "\n=== Proyecto '$nombre' creado correctamente ==="
puts "=== Abrir con: vivado [file join $dir_proyecto ${nombre}.xpr] ===\n"
