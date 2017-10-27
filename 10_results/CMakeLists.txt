add_inputs(chapter.tex)

#
# Tables
#
add_custom_target(
        table_reference
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/table_reference/make_table.py
        COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS
        ${CMAKE_CURRENT_LIST_DIR}/table_reference/make_table.py
        ${CMAKE_CURRENT_LIST_DIR}/HF_reference/data.yaml
)
add_depends(table_reference)

add_custom_target(
        table_kopt
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/table_kopt/make_table.py
        COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS
        ${CMAKE_CURRENT_LIST_DIR}/table_kopt/make_table.py
        ${CMAKE_CURRENT_LIST_DIR}/HF_reference/data.yaml
)
add_depends(table_kopt)

#
# Images
#
set(PDF_OUTPUTS "")

#
# nlm dependence
#
# Plot EHF vs shell
set(PDF_OUTPUTS ${PDF_OUTPUTS} Delta_EHF_vs_shell.pdf)
add_custom_command(
        OUTPUT Delta_EHF_vs_shell.pdf
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/E_vs_shell/plot.py
        COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_shell/plot.py
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_shell/Li_results.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_shell/Be_results.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_shell/B_results.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_shell/C_results.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_shell/N_results.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_shell/O_results.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_shell/F_results.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_shell/Ne_results.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/HF_reference/data.yaml
)

# Plot RMSO vs l for period 1, 2 and the ions
set(PDF_OUTPUTS ${PDF_OUTPUTS}
        rmso_period2_vs_l.pdf rmso_period3_vs_l.pdf rmso_ions_vs_l.pdf
        rms_lf_C.pdf rms_lf_N.pdf rms_lf_O.pdf
)
add_custom_command(
        OUTPUT
        rmso_period2_vs_l.pdf rmso_period3_vs_l.pdf rmso_ions_vs_l.pdf
        rms_lf_C.pdf rms_lf_N.pdf rms_lf_O.pdf
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/RMSO_vs_l/plot.py
        COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS
        ${CMAKE_CURRENT_LIST_DIR}/RMSO_vs_l/plot.py
        ${CMAKE_CURRENT_LIST_DIR}/RMSO_vs_l/rmsl.py
)

# Plot orbital energies wrt nlm
set(PDF_OUTPUTS ${PDF_OUTPUTS} orben_vs_nlm_N.pdf ehf_vs_nlm.pdf ehf_vs_nlm_O.pdf
)
add_custom_command(
        OUTPUT orben_vs_nlm_N.pdf ehf_vs_nlm.pdf ehf_vs_nlm_O.pdf
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/E_vs_nlm/plot.py
        COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_nlm/plot.py
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_nlm/Be_plot_data.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_nlm/O_plot_data.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_nlm/N_plot_data.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_nlm/P_plot_data.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/HF_reference/data.yaml
)

# Plot Be correlation energy
set(PDF_OUTPUTS ${PDF_OUTPUTS} Be_fci_cc_vs_nbas.pdf)
add_custom_command(
        OUTPUT Be_fci_cc_vs_nbas.pdf
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/Ecc_be_fci/plot.py
        COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/Ecc_be_fci/plot.py
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/Ecc_be_fci/Be_fci_high_accuracy.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/Ecc_be_fci/Be_fci_summary.yaml
)

# Plot change in correlation energies
set(PDF_OUTPUTS ${PDF_OUTPUTS}
        Etot_vs_bas_easy.pdf Etot_vs_bas_hard.pdf Ecc_vs_bas_hard.pdf Ecc_vs_bas_easy.pdf
)
add_custom_command(
        OUTPUT Etot_vs_bas_easy.pdf Etot_vs_bas_hard.pdf Ecc_vs_bas_hard.pdf Ecc_vs_bas_easy.pdf
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/Ecc_vs_nlm/plot.py
        COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/Ecc_vs_nlm/plot.py
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/Ecc_vs_nlm/summary.yaml
)

#
# k dependence
#
# Plot HF, MP2, FCI vs k
set(PDF_OUTPUTS ${PDF_OUTPUTS} Efci_vs_k.pdf EHF_terms_vs_k.pdf)
add_custom_command(
        OUTPUT Efci_vs_k.pdf EHF_terms_vs_k.pdf
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/Efci_vs_k/plot.py
        COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/Efci_vs_k/plot.py
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/Efci_vs_k/summary.yaml
)

# Plot HF vs k for carbon
set(PDF_OUTPUTS ${PDF_OUTPUTS} C_ene_gs_vs_k.pdf C_hfterms_vs_k.pdf C_orben_622_vs_k.pdf)
add_custom_command(
        OUTPUT C_ene_gs_vs_k.pdf C_hfterms_vs_k.pdf C_orben_622_vs_k.pdf
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/E_vs_k/plot.py
        COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_k/plot.py
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_k/C_n6-l2-m2-summary.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_k/C_n5-l2-m2-summary.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/E_vs_k/C_n4-l2-m2-summary.yaml
)

# Plot kopt vs atomic number (and Zeff)
set(PDF_OUTPUTS ${PDF_OUTPUTS} kopt_vs_atnum.pdf)
add_custom_command(
        OUTPUT kopt_vs_atnum.pdf
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/kopt_vs_atnum/plot_kopt_vs_atnum.py
        COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/kopt_vs_atnum/plot_kopt_vs_atnum.py
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/kopt_vs_atnum/Zeff.yaml
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/kopt_vs_atnum/summary.yaml
)

foreach(out ${PDF_OUTPUTS})
        pdf_image(${CMAKE_CURRENT_BINARY_DIR}/${out} TMP)
        add_depends(${TMP})
endforeach()
