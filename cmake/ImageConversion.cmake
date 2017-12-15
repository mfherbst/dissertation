set(IMAGE_FORMAT "pdf" CACHE STRING
	"The format to use for images.")

set(TIKZ_IMAGE_MODULE_DIR "${CMAKE_CURRENT_LIST_DIR}" CACHE INTERNAL
	"Directory where the TikzImage module is located." FORCE)

set(Python_ADDITIONAL_VERSIONS 3)
find_package(PythonInterp REQUIRED)

function(tikz_image INFILE DEPENDVAR)
	# INFILE      tikz file to convert to pdf or png format
	# DEPENDVAR   variable to which to add the dependent files

	if (NOT IS_ABSOLUTE "${INFILE}")
		set(INFILE_ABS "${CMAKE_CURRENT_LIST_DIR}/${INFILE}")
	else()
		set(INFILE_ABS "${INFILE}")
	endif()

	if (NOT EXISTS "${INFILE_ABS}")
		message(FATAL_ERROR "File ${INFILE} does not exist.")
	endif()

	# Make tex file to compile to standalone pdf image
	get_filename_component(INFILE_NOTIKZ "${INFILE}" NAME_WE)
	set(GENERATED_TEX_FILE "${INFILE_NOTIKZ}.tex")
	add_custom_command(
		OUTPUT "${GENERATED_TEX_FILE}"
		COMMAND ${PYTHON_EXECUTABLE}
		ARGS "${TIKZ_IMAGE_MODULE_DIR}/convert_tikz.py"
		"${INFILE_ABS}" "${GENERATED_TEX_FILE}"
		DEPENDS
		"${INFILE_ABS}"
		"${TIKZ_IMAGE_MODULE_DIR}/convert_tikz.py"
	)

	set(CUSTPACKDEP "")
	foreach(custpack ${MFH_LATEX_CUSTOM_PACKAGES})
		add_custom_command(
			OUTPUT "${custpack}.sty"
			COMMAND
			${CMAKE_COMMAND} -E copy
				"${MFH_LATEX_BINARY_DIR}/${custpack}.sty" ${custpack}.sty
			DEPENDS
			"${custpack}_copy"
		)
		set(CUSTPACKDEP ${CUSTPACKDEP} ${custpack}.sty)
	endforeach()

	# Make the actual pdf image
	add_latex_document("${GENERATED_TEX_FILE}" EXCLUDE_FROM_ALL
		DEPENDS "${GENERATED_TEX_FILE};${CUSTPACKDEP}")
	latex_get_output_path(OUTPUT)
	set(GENERATED_PDF_FILE "${OUTPUT}/${INFILE_NOTIKZ}.pdf")

	if ("${IMAGE_FORMAT}" STREQUAL "pdf")
		set(${DEPENDVAR} ${${DEPENDVAR}} "${INFILE_NOTIKZ}_pdf" PARENT_SCOPE)
	else()
		pdf_image(${GENERATED_PDF_FILE} TTMP)
		set(${DEPENDVAR} ${${DEPENDVAR}} ${TTMP} PARENT_SCOPE)
	endif()
endfunction()

function(pdf_image INFILE DEPENDVAR)
	if (NOT IS_ABSOLUTE "${INFILE}")
		set(INFILE "${CMAKE_CURRENT_LIST_DIR}/${INFILE}")
	endif()

	# Build taget path for pdf and png
	get_filename_component(INFILE_NOPDF "${INFILE}" NAME_WE)
	get_filename_component(INFILE_DIR "${INFILE}" DIRECTORY)
	set(PDF_FILE "${CMAKE_CURRENT_BINARY_DIR}/${INFILE_NOPDF}.pdf")
	set(PNG_FILE "${CMAKE_CURRENT_BINARY_DIR}/${INFILE_NOPDF}.png")

	# TODO This method stops working as soon as we need images from subdirectories

	if (INFILE_DIR STREQUAL CMAKE_CURRENT_BINARY_DIR)
		# pdf is already in build dir
		# => nothing to do
		set(PDF_FILE "${INFILE}")
	elseif (INFILE_DIR STREQUAL CMAKE_CURRENT_LIST_DIR)
		# Copy pdf file into build dir
		add_custom_command(
			OUTPUT "${PDF_FILE}"
			COMMAND ${CMAKE_COMMAND} -E copy "${INFILE}" "${PDF_FILE}"
			COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
			DEPENDS
			"${INFILE}"
		)
	else()
		message(FATAL_ERROR "INFILE ${INFILE} needs to be either below the build or the source directory or alternatively a relative path into the source directory.")
	endif()

	if ("${IMAGE_FORMAT}" STREQUAL "pdf")
		add_custom_target(${INFILE_NOPDF}_pdf
			DEPENDS
			"${PDF_FILE}"
		)
		set(${DEPENDVAR} ${${DEPENDVAR}} "${INFILE_NOPDF}_pdf" PARENT_SCOPE)
	elseif("${IMAGE_FORMAT}" STREQUAL "png")
		add_custom_command(
			OUTPUT "${PNG_FILE}"
			COMMAND "${TIKZ_IMAGE_MODULE_DIR}/pdf_to_pdfa_png.sh" "${PDF_FILE}" "${PNG_FILE}"
			COMMAND ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
			DEPENDS
			"${PDF_FILE}"
			"${TIKZ_IMAGE_MODULE_DIR}/pdf_to_pdfa_png.sh"
		)
		add_custom_target(${INFILE_NOPDF}_png DEPENDS "${PNG_FILE}")
		set(${DEPENDVAR} ${${DEPENDVAR}} "${INFILE_NOPDF}_png" PARENT_SCOPE)
	else()
		message(FATAL_ERROR "Image format not implemented: ${IMAGE_FORMAT}")
	endif()
endfunction()
