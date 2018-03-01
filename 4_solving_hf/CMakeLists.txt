add_inputs(
	chapter.tex
	scf_overview.tex
	guess.tex
	scf_algos.tex
	functions.tex
	functions_sto.tex
	functions_cgto.tex
	functions_fe.tex
	functions_cs.tex
	summary.tex
)

#
# TikZ images
#
tikz_image(roothaan_oda.tikz TMP)
add_depends(${TMP})
tikz_image(gdm.tikz TMP)
add_depends(${TMP})

#
# Python pdf images
#
set(PDF_OUTPUTS "")

# H2 UMP2 dissociation example plot
set(PDF_OUTPUTS ${PDF_OUTPUTS}
        fock_sturmian.pdf fock_gaussian.pdf fock_fe.pdf
)
add_custom_command(
        OUTPUT
        fock_sturmian.pdf fock_gaussian.pdf fock_fe.pdf
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/fock_matrices/plot_fock.py
        COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/fock_matrices/plot_fock.py
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/fock_matrices/common.py
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/fock_matrices/Be_sturmian_511.hdf5
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/fock_matrices/Be_gaussian_pc2.hdf5
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/fock_matrices/fock_fe.pdf
)

set(PDF_OUTPUTS ${PDF_OUTPUTS}
	local_energy_cgto.pdf local_energy_cgto_zoom.pdf relative_error_cgto.pdf
)
add_custom_command(
	OUTPUT
	local_energy_cgto.pdf local_energy_cgto_zoom.pdf relative_error_cgto.pdf
	COMMAND ${CMAKE_CURRENT_LIST_DIR}/hydrogen_comparison/cgtos.py
	COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
	DEPENDS ${CMAKE_CURRENT_LIST_DIR}/hydrogen_comparison/cgtos.py
	DEPENDS ${CMAKE_CURRENT_LIST_DIR}/hydrogen_comparison/common.py
)

set(PDF_OUTPUTS ${PDF_OUTPUTS}
	local_energy_cs.pdf local_energy_cs_zoom.pdf relative_error_cs.pdf
)
add_custom_command(
	OUTPUT
	local_energy_cs.pdf local_energy_cs_zoom.pdf relative_error_cs.pdf
	COMMAND ${CMAKE_CURRENT_LIST_DIR}/hydrogen_comparison/cs.py
	COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
	DEPENDS ${CMAKE_CURRENT_LIST_DIR}/hydrogen_comparison/cs.py
	DEPENDS ${CMAKE_CURRENT_LIST_DIR}/hydrogen_comparison/common.py
)

set(PDF_OUTPUTS ${PDF_OUTPUTS}
	fe_grid_linear.pdf fe_grid_quadratic.pdf
)
add_custom_command(
	OUTPUT
	fe_grid_linear.pdf fe_grid_quadratic.pdf
	COMMAND ${CMAKE_CURRENT_LIST_DIR}/plot_fe_grid.py
	COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
	DEPENDS ${CMAKE_CURRENT_LIST_DIR}/plot_fe_grid.py
)

set(PDF_OUTPUTS ${PDF_OUTPUTS}
	shape_functions_1d.pdf shape_functions_2d.pdf
)
add_custom_command(
	OUTPUT
	shape_functions_1d.pdf shape_functions_2d.pdf
	COMMAND ${CMAKE_CURRENT_LIST_DIR}/plot_shape_functions.py
	COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
	DEPENDS ${CMAKE_CURRENT_LIST_DIR}/plot_shape_functions.py
)

set(PDF_OUTPUTS ${PDF_OUTPUTS} fock_fe_gauss_sturm.pdf)
add_custom_command(
	OUTPUT fock_fe_gauss_sturm.pdf
	COMMAND ${CMAKE_COMMAND} -E copy
	${CMAKE_CURRENT_LIST_DIR}/fock_matrices/fock_fe_gauss_sturm.pdf
	${CMAKE_CURRENT_BINARY_DIR}
	COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
	DEPENDS ${CMAKE_CURRENT_LIST_DIR}/fock_matrices/fock_fe_gauss_sturm.pdf
)

foreach(out ${PDF_OUTPUTS})
        pdf_image(${CMAKE_CURRENT_BINARY_DIR}/${out} TMP)
        add_depends(${TMP})
endforeach()

