add_inputs(chapter.tex)
add_inputs(tise.tex)
add_inputs(fci.tex)
add_inputs(hf_intro.tex)
add_inputs(correlation.tex)
add_inputs(dft.tex)


#
# TikZ images
#
tikz_image(fci_matrix.tikz TMP)
add_depends(${TMP})
