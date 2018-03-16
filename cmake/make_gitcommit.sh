#!/bin/bash
{
	COMMIT=$(git rev-parse HEAD)
	TAG=$(git tag --points-at $COMMIT)

	echo '\newcommand{\gitcommit}{'$COMMIT'}'
	if [ "$TAG" ]; then
		echo '\newcommand{\gittag}{'$TAG'}'
		echo '\newcommand{\gitcurrent}{tag \texttt{'$TAG'}\xspace}'
	else
		echo '\newcommand{\gittag}{}'
		echo '\newcommand{\gitcurrent}{commit \texttt{'$COMMIT'}\xspace}'
	fi
} > gitcommit.tex
