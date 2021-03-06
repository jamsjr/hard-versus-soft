
set terminal post enh
set output "data/rthisto1.eps"

set yrange[1:10000]
set xrange[-0.1:1.1]

set log y
set xlabel "Response time"
set ylabel "Frequency"
set grid

plot "data/soft-l1-response_time-histo.data" using 1:2 title "" with impulses lw 4

