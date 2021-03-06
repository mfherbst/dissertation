add_inputs(
	chapter.tex
	contraction.tex
	lazy.tex
)
add_inputs(rhf_code.cpp)

#
# TikZ images
#
foreach(TIMG lazyten_structure expression_tree expression_tree2)
	tikz_image(${TIMG}.tikz TMP)
	add_depends(${TMP})
endforeach()


#
# Python pdf images
#
set(PDF_OUTPUTS "")

# H2 UMP2 dissociation example plot
set(PDF_OUTPUTS ${PDF_OUTPUTS} mem_cpu_years.pdf)
add_custom_command(
        OUTPUT mem_cpu_years.pdf
        COMMAND ${CMAKE_CURRENT_LIST_DIR}/memcpu/plot.py
        COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/memcpu/plot.py
        DEPENDS ${CMAKE_CURRENT_LIST_DIR}/memcpu/data.yaml
)



foreach(out ${PDF_OUTPUTS})
        pdf_image(${CMAKE_CURRENT_BINARY_DIR}/${out} TMP)
        add_depends(${TMP})
endforeach()
