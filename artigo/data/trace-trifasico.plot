
set terminal post enh
set output "data/trace-trifasico.eps"

set yrange[0:0.8]

set grid

plot "../src/data/trifasico.txt" using 1:2 title "" with points
