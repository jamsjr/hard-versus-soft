
set terminal post enh
set output "data/trifasico-2.eps"

set yrange[0:1]

set grid

plot "data/hard-adaptive-response_time-points.data" using 1:2 title "" with points
