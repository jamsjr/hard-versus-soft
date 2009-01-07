
set terminal post enh
set output "data/rthisto2.eps"

set yrange[0:1000]
set xrange[0:1]

set grid

plot "data/hard-l1-response_time-histo.data" using 1:2 title "Hard reservation" with impulses lw 4

