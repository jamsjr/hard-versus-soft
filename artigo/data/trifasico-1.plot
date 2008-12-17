
set terminal post enh
set output "data/trifasico-1.eps"

set yrange[0:1]

set grid
set xlabel "Time"
set ylabel "Response time"

plot "data/soft-adaptive-response_time-points.data" using 1:2 title "Soft reservation" with points

