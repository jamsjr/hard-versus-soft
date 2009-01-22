
set terminal post enh
set output "data/dthisto2.eps"

set yrange[0:1000]
set xrange[-0.1:1.1]

set grid

plot "data/hard-l1-delay_time-histo.data" using 1:2 title "" with impulses lw 4

