#!/bin/bash

FROM=$1
TO=$2

RESOLUTION="-scale-to 5000" #px
if [ -z "$FROM" -o -z "$TO" ]; then
	echo "You need to specify 2 arguments: pdf to convert from, png to convert to." >&2
	exit 1
fi

TEMP=$(mktemp)
pdftoppm -png $RESOLUTION "$FROM" > "$TEMP"
convert "$TEMP" -colorspace sRGB -background white -alpha off -alpha remove "$TO"
rm "$TEMP"
