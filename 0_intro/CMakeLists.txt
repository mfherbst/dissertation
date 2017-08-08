add_inputs(chapter.tex)

# Test tikz image
tikz_image(tester.tikz TMP)
add_depends(${TMP})
