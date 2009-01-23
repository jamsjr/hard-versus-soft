
set terminal post enh
set output "data/trace-eve.eps"

set yrange[0:0.03]
set xlabel "Release Time"
set ylabel "Cost"

set grid

plot "../src/data/decode-trace-eve.txt" using 1:2 title "" with points
