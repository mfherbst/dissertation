#!/usr/bin/awk -f

BEGINFILE {
	n = substr(FILENAME, 0, length(FILENAME) - 6)
	l = substr(FILENAME, length(FILENAME) - 5, 1)
	m = substr(FILENAME, length(FILENAME) - 4, 1)
	print "- kexp: 2.0"
	print "  nmax: " n
	print "  lmax: " l
	print "  mmax: " m

	count = 0
}

function map(a) {
	switch(a) {
		case 1:
			return "1s"
		case 2:
			return "2s"
		case 3:
		case 4:
		case 5:
			return "2p"
		case 6:
			return "3s"
		case 7:
		case 8:
		case 9:
			return "3p"
		case 10:
			return "4s"
		case 11:
		case 12:
		case 13:
			return "4p"
	}
	return a
}

/MP.2. Summary/ { inside_mp=1 }
/Total energy:/ && inside_mp {
	inside_mp=0
	print "  ground_state: " $3
	print "  singlets:"
}

/^ *Excited state / { inside_block=1; state_number=$3 }
inside_block==1 && /^ *Term symbol/ { term_symbol=$3 " " $4 " " $5; spin = $4 }
inside_block==1 && /^ *Total energy/ { energy=$3 }
inside_block==1 && /^ *Important amplitudes/ { ampl=1; next }

inside_block==1 && ampl==1 && /A/ {
	if (spin == "(1)") {
		if (NF == 7) {
			print "    - " energy "  # " count " " map($1) " -> " map($4)
		} else {
			printf "    - " energy "  # " count " " map($1) "," map($4)
			print " -> " map($7) "," map($10)
		}
		count++
	}

	inside_block=0
	ampl=0
	from=""
	to=""
}
