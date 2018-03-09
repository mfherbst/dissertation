add_inputs(
	main.tex
)

#
# Build lists
#
add_custom_target(
	make_appendix_lists
        COMMAND
        ${PYTHON_EXECUTABLE}
        ${CMAKE_CURRENT_LIST_DIR}/make_appendix_lists.py
        COMMAND
        ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS
        ${CMAKE_CURRENT_LIST_DIR}/make_appendix_lists.py
)
add_depends(make_appendix_lists)
