cmake_minimum_required(VERSION 3.0.0)
cmake_policy(VERSION 3.0.0)

# Start project and include the modules we need
project(Dissertation NONE)
include(cmake/UseLATEX/UseLATEX.cmake)
include(cmake/TexInputs.cmake)
include(cmake/ImageConversion.cmake)

# Make sure the documentclasses and tex packages we require
# from mfhTex are found
# This needs to be called before doing anything with the
# commands provided by cmake/ImageConversion.cmake
add_custom_documentclasses(mfhTex/mfh/MFHbook.cls)

add_custom_packages(
	mfhTex/mfh/MFHabbr.sty
	mfhTex/mfh/MFHcode.sty
	mfhTex/mfh/MFHcolours.sty
	mfhTex/mfh/MFHdefault.sty
	mfhTex/mfh/MFHscience.sty
	mfhTex/mfh/MFHtheoremdefs.sty
)

# Dump info about the git repo status
add_custom_target(
	make_gitcommit
        COMMAND
        ${CMAKE_CURRENT_LIST_DIR}/cmake/make_gitcommit.sh
        COMMAND
        ${CMAKE_COMMAND} -E touch "${MFH_LATEX_TOUCHFILE}"
)
add_depends(make_gitcommit)


# Tex files
add_inputs(
	abstract.tex
	biblio.tex
	common_commands.tex
	common_configure.tex
	common_packages.tex
	commands.tex
	contents.tex
	dedication.tex
	hyphenation.tex
	index.tex
	licence.tex
	nomenclature.tex
        publications.tex
	title.tex
	versicherung.tex
	#
	metadata.xmp
)

# Images and other dependencies
pdf_image(cc-by-sa.pdf CCBYSA)
add_depends(${CCBYSA})

add_subdirectory(0_intro)
add_subdirectory(1_qm)
add_subdirectory(2_numeigen)
add_subdirectory(3_qchem)
add_subdirectory(4_solving_hf)
add_subdirectory(6_contraction_lazy_matrices)
add_subdirectory(8_molsturm)
add_subdirectory(10_results)
add_subdirectory(13_conclusion)
add_subdirectory(15_future)
add_subdirectory(42_appendix)
add_subdirectory(99_acknowledgements)

add_latex_document(dissertation.tex
	INPUTS ${MFH_LATEX_INPUTS}
	BIBFILES references.bib
	CONFIGURE common_configure.tex
	IMAGES ${MFH_LATEX_IMAGES}
	# inputs should also specify code files which are included into the tex source
	DEPENDS ${MFH_LATEX_DEPENDS}
	# Use nomenclature and index
	USE_NOMENCL
	USE_INDEX
)
