add_inputs(
        appendix.tex
        eri_symmetries.tex
	hf_theorem_finite.tex
        cbs_uhf.tex
        rmso_Gaussian.tex
        cs_convergence.tex
	molsturm_output.tex
)
add_inputs(molsturm_output.out molsturm_input.py)

#
# Build tables
#
add_custom_target(
        table_cs_corr_conv
        COMMAND
        ${PYTHON_EXECUTABLE}
        ${CMAKE_CURRENT_LIST_DIR}/table_cs_corr_conv/make_table.py
        COMMAND
        ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS
        ${CMAKE_CURRENT_LIST_DIR}/table_cs_corr_conv/make_table.py
        ${CMAKE_CURRENT_LIST_DIR}/table_cs_corr_conv/summary.yaml
)
add_depends(table_cs_corr_conv)

add_custom_target(
        table_Be_CS_hf_mp2_fci
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/table_Be_CS_hf_mp2_fci/make_table.py
        COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS
        ${CMAKE_CURRENT_LIST_DIR}/table_Be_CS_hf_mp2_fci/make_table.py
        ${CMAKE_CURRENT_LIST_DIR}/table_Be_CS_hf_mp2_fci/Be_fci_summary.yaml
        ${CMAKE_CURRENT_LIST_DIR}/table_Be_CS_hf_mp2_fci/Be_fci_high_accuracy.yaml
)
add_depends(table_Be_CS_hf_mp2_fci)


#
# Plot images
#
set(PDF_OUTPUTS "")

# Plot Gaussian RMSO vs l
set(PDF_OUTPUTS ${PDF_OUTPUTS}
        ccpvnz_rmso_period2_vs_l.pdf ccpvnz_rmso_period3_vs_l.pdf
        ccpvnz_rms_lf_C.pdf ccpvnz_rms_lf_N.pdf ccpvnz_rms_lf_O.pdf
)
add_custom_command(
        OUTPUT
        ccpvnz_rmso_period2_vs_l.pdf ccpvnz_rmso_period3_vs_l.pdf
        ccpvnz_rms_lf_C.pdf ccpvnz_rms_lf_N.pdf ccpvnz_rms_lf_O.pdf
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/RMSO_vs_l_ccpvnz/plot.py
        COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS
        ${CMAKE_CURRENT_LIST_DIR}/RMSO_vs_l_ccpvnz/plot.py
)

foreach(out ${PDF_OUTPUTS})
        pdf_image(${CMAKE_CURRENT_BINARY_DIR}/${out} TMP)
        add_depends(${TMP})
endforeach()
