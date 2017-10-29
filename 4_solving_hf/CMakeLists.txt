add_inputs(chapter.tex)

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


foreach(out ${PDF_OUTPUTS})
        pdf_image(${CMAKE_CURRENT_BINARY_DIR}/${out} TMP)
        add_depends(${TMP})
endforeach()
