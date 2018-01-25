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
)

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


foreach(out ${PDF_OUTPUTS})
        pdf_image(${CMAKE_CURRENT_BINARY_DIR}/${out} TMP)
        add_depends(${TMP})
endforeach()
