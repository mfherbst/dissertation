latex_get_output_path(MFH_LATEX_BINARY_DIR)
set(MFH_LATEX_SOURCE_DIR "${PROJECT_SOURCE_DIR}")

# Empty and reset relevant cache variables
set(MFH_LATEX_TOUCHFILE "${MFH_LATEX_BINARY_DIR}/force_rebuild.touch")
set(MFH_LATEX_INPUTS  "" CACHE INTERNAL  "Accumulator for static input files" FORCE)
set(MFH_LATEX_DEPENDS "${MFH_LATEX_TOUCHFILE}"
	CACHE INTERNAL "Accumulator for dependent files" FORCE)
set(MFH_LATEX_IMAGES  "" CACHE INTERNAL  "Accumulator for images" FORCE)

# Setup an empty touchfile
file(WRITE "${MFH_LATEX_TOUCHFILE}" "")

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

