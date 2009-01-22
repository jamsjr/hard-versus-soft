
set terminal post enh
set output "data/variance-1.eps"

set yrange[0:1.1]

set grid

plot "data/soft-variance-response_time-points.data" using 1:2 title "" with points

