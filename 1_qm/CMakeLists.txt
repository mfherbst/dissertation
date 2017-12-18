add_inputs(chapter.tex)
add_inputs(correspondence.tex)
add_inputs(funcana.tex)
add_inputs(spectral.tex)
add_inputs(takeaway.tex)

#
# TikZ images
#
tikz_image(sobolev.tikz TMP)
add_depends(${TMP})
