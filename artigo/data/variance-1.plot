
set terminal post enh
set output "data/variance-1.eps"

set yrange[0:1.1]

set grid
set xlabel "Time"
set ylabel "Response time"

plot "data/soft-variance-response_time-points.data" using 1:2 title "Soft reservation" with points

