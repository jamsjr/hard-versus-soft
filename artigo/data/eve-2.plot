
set terminal post enh
set output "data/eve-2.eps"

set yrange[0:0.1]
set xlabel "Release Time"
set ylabel "Wait time"

set grid

plot "data/hard-eve-delay_time-points.data" using 1:2 title "" with points

