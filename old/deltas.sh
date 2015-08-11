#WHERE		CART		RF
precision() { cat<<EOF | sed 's?\\t\\t?\\t?g' | cat -n 
-30		-24		-43
-10		-5		-15
-2		-1		-3
0		1		-2
0		3		-2
0		3		-1
5		3		0
6		6		0
6		7		0
7		7		1
13		15		1
40		16		3
42		16		5
59		29		11
63		33		19
72		58		21
96		62		50
EOF
	    }
#WHERE				CART                             RF
F() { cat <<EOF | sed 's?\\t\\t\\t?\\t?g' | cat -n 
-14				-43				-27
-14				-6				-10
-6				-2				-4
-5				-1				-4
-4				1				-3
-2				2				-2
0				5				-2
0				6				-2
2				6				0
4				8				0
5				12				1
6				13				2
7				16				2
14				19				2
28				19				4
73				35				5
87				57				5
EOF
}
precision > /tmp/precision.dat
F > /tmp/F.dat

draw() {
gnuplot<<EOF
set key bottom right
set output "${1}1.eps
set title "$1"
set terminal postscript eps color "Helvetica" 15
set size 0.3,0.75
set yrange [-100:100]
set ytics (-50,0,50,100)
set xlabel "Improvements, sorted"
set xtics (1,4,8,12,17)
set arrow 1 from 1,0 to 17,0 nohead
plot "/tmp/$1.dat" using 1:2 title "WHERE"  with linesp,\
     "/tmp/$1.dat"  using 1:3 title "CART" with linesp,\
     "/tmp/$1.dat"  using 1:4 title "R.Forest" with linesp,
EOF
ps2pdf -dEPSCrop ${1}1.eps 
}

draw precision 
draw F
