add_inputs(
    chapter.tex
    related.tex
    design.tex
    examples.tex
    examples/ccd/ccd_eqn_vs_code.tex
    state.tex
    takeaway.tex
    #
    examples/dissociation/h2_dissociation.py
    examples/ccd/ccd.py
    examples/geo_opt.py
)
add_images(8_molsturm/h2o_density.png)

#
# TikZ images
#
tikz_image(molsturm_structure.tikz TMP)
add_depends(${TMP})

#
# Python pdf images
#
set(PDF_OUTPUTS "")

# H2 UMP2 dissociation example plot
set(PDF_OUTPUTS ${PDF_OUTPUTS} h2_dissociation.pdf)
add_custom_command(
        OUTPUT h2_dissociation.pdf
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/examples/dissociation/plot.py
        COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/examples/dissociation/plot.py
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/examples/dissociation/H2_UMP2_dissociation.yaml
)



foreach(out ${PDF_OUTPUTS})
        pdf_image(${CMAKE_CURRENT_BINARY_DIR}/${out} TMP)
        add_depends(${TMP})
endforeach()
