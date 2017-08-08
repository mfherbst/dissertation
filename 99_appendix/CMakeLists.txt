add_inputs(appendix.tex)

#
# Build tables
#
add_custom_target(
        tables_CS_hf_mp2
        COMMAND
        ${PYTHON_EXECUTABLE}
        ${CMAKE_CURRENT_LIST_DIR}/CS_hf_mp2_nlm_tables/make_tables.py
        COMMAND
        ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
        DEPENDS
        ${CMAKE_CURRENT_LIST_DIR}/CS_hf_mp2_nlm_tables/make_tables.py
        ${CMAKE_CURRENT_LIST_DIR}/CS_hf_mp2_nlm_tables/summary.yaml
)
add_depends(tables_CS_hf_mp2)
