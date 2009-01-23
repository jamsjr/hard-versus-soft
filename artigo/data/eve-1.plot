
set terminal post enh
set output "data/eve-1.eps"

set yrange[0:0.1]
set xlabel "Release Time"
set ylabel "Wait time"
set grid

plot "data/soft-eve-delay_time-points.data" using 1:2 title "" with points

