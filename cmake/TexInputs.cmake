macro(mfh_latex_reset)
	# Reset the state of the MFH_LATEX_ variables
	latex_get_output_path(MFH_LATEX_BINARY_DIR)
	set(MFH_LATEX_SOURCE_DIR "${PROJECT_SOURCE_DIR}")

	# Empty and reset relevant cache variables
	set(MFH_LATEX_TOUCHFILE "${MFH_LATEX_BINARY_DIR}/force_rebuild.touch")
	set(MFH_LATEX_INPUTS  "" CACHE INTERNAL  "Accumulator for static input files" FORCE)
	set(MFH_LATEX_DEPENDS "${MFH_LATEX_TOUCHFILE}"
		CACHE INTERNAL "Accumulator for dependent files" FORCE)
	set(MFH_LATEX_IMAGES  "" CACHE INTERNAL  "Accumulator for images" FORCE)

	set(MFH_LATEX_CUSTOM_PACKAGES "" CACHE INTERNAL  "Accumulator for custom latex packages" FORCE)

	# Setup an empty touchfile
	file(WRITE "${MFH_LATEX_TOUCHFILE}" "")
endmacro()

#
# Helper functions
#

function(relative_from_source IN OUT)
	# Transform a path inside the source tree relative to the topmost source directory
	if (NOT IS_ABSOLUTE "${IN}")
		set(IN "${CMAKE_CURRENT_LIST_DIR}/${IN}")
	endif()
	file(RELATIVE_PATH TMP "${MFH_LATEX_SOURCE_DIR}" "${IN}")
	set(${OUT} "${TMP}" PARENT_SCOPE)
endfunction()

function(relative_from_binary IN OUT)
	# Transform a path inside the binary tree relative to the topmost source directory
	if (NOT IS_ABSOLUTE "${IN}")
		set(IN "${CMAKE_CURRENT_BINARY_DIR}/${IN}")
	endif()
        # Note: MFH_LATEX_SOURCE_DIR is on purpose here!
        file(RELATIVE_PATH TMP "${MFH_LATEX_SOURCE_DIR}" "${IN}")
	set(${OUT} "${TMP}" PARENT_SCOPE)
endfunction()

function(copy_to_latex_binary_dir INFILE DEPENDVAR)
	# Copy a file exactly into the latex binary dir
	# (i.e. the top directory and no other)
	if (NOT IS_ABSOLUTE "${INFILE}")
		set(INFILE_ABS "${CMAKE_CURRENT_LIST_DIR}/${INFILE}")
	else()
		set(INFILE_ABS "${INFILE}")
	endif()

	get_filename_component(INFILE_NAME "${INFILE_ABS}" NAME)
	get_filename_component(INFILE_NOEXT "${INFILE_ABS}" NAME_WE)
	set(INFILE_NAME "${MFH_LATEX_BINARY_DIR}/${INFILE_NAME}")

	add_custom_command(
		OUTPUT "${INFILE_NAME}"
		COMMAND ${CMAKE_COMMAND} -E copy ${INFILE_ABS} ${INFILE_NAME}
		COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
		DEPENDS
		${INFILE_ABS}
	)
	add_custom_target(${INFILE_NOEXT}_copy DEPENDS "${INFILE_NAME}")

	set(${DEPENDVAR} ${${DEPENDVAR}} "${INFILE_NOEXT}_copy" PARENT_SCOPE)
endfunction()

#
# Add functions
#

function(add_inputs)
	foreach(arg ${ARGN})
		relative_from_source("${arg}" OUT)
		set(MFH_LATEX_INPUTS ${MFH_LATEX_INPUTS} ${OUT} CACHE INTERNAL "Accumulator for static input files" FORCE)
	endforeach()
endfunction()

function(add_depends)
	foreach(arg ${ARGN})
		relative_from_binary("${arg}" OUT)
		set(MFH_LATEX_DEPENDS ${MFH_LATEX_DEPENDS} ${OUT} CACHE INTERNAL "Accumulator for dependend files" FORCE)
	endforeach()
endfunction()

function(add_images)
	set(MFH_LATEX_IMAGES ${MFH_LATEX_IMAGES} ${ARGN} CACHE INTERNAL "Accumulator for images" FORCE)
endfunction()

function(add_custom_packages)
	# Add custom latex sty packages to be used
	foreach(arg ${ARGN})
		copy_to_latex_binary_dir(${arg} TEMP)
		add_depends(${TEMP})

		get_filename_component(ARG_NOEXT "${arg}" NAME_WE)
		set(MFH_LATEX_CUSTOM_PACKAGES ${MFH_LATEX_CUSTOM_PACKAGES} ${ARG_NOEXT}
			CACHE INTERNAL "Accumulator for custom latex packages")
	endforeach()
endfunction()

function(add_custom_documentclasses)
	# Add custom latex cls classes to be used
	foreach(arg ${ARGN})
		copy_to_latex_binary_dir(${arg} TEMP)
		add_depends(${TEMP})
	endforeach()
endfunction()

#
# Call the setup macro
#
mfh_latex_reset()
