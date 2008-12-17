
set terminal post enh
set output "data/trace-trifasico.eps"

set yrange[0:0.8]

set grid
set xlabel "Time"
set ylabel "Costs"

plot "../src/data/trifasico.txt" using 1:2 title "Varying costs." with points
