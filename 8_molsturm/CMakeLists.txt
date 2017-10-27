add_inputs(chapter.tex)

#
# TikZ images
#
tikz_image(molsturm_structure.tikz TMP)
add_depends(${TMP})
