
set terminal post enh
set output "data/trace-variance.eps"

set yrange[0:0.8]

set grid

plot "../src/data/norm-0.5-variance.txt" using 1:2 title "" with points
