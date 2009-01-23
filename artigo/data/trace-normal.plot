
set terminal post enh
set output "data/trace-normal.eps"

set yrange[0:0.8]
set xlabel "Release Time"
set ylabel "Cost"

set grid

plot "../src/data/norm-0.4.txt" using 1:2 title "" with points
