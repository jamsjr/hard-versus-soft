

set terminal post enh
set output "data/variance-2.eps"

set xlabel "Release Time"
set ylabel "Response time"
set yrange[0:1.1]

set grid

plot "data/hard-variance-response_time-points.data" using 1:2 title "" with points

