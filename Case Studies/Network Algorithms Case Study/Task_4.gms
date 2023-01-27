sets
p plants /1*2/
w warehouses (and dummy)/1*3/
r retail stores (and dummy) /1*16/
;

parameters
s(p) supply of plant p (in 1000 packets)
/
"1" = 12000,
"2" = 5000
/

d(r) demand of retail store r (in 1000 packets)
/
"1" = 500,
"2" = 1000,
"3" = 200,
"4" = 700,
"5" = 1400,
"6" = 1200,
"7" = 900,
"8" = 400,
"9" = 1800,
"10" = 2100,
"11" = 600,
"12" = 1300,
"13" = 100,
"14" = 1500,
"15" = 2000,
"16" = 300
/

*c capacity of a warehouse /8000/
;

table t_p2w(p, w) transportation costs per 1000 packets from plants to warehouses
         1       2       3
1        1       9       12
2        8       13      6
;

table t_w2r(w, r) transportation costs per 1000 packets from warehouses to retail stores
         1       2       3       4       5       6       7       8       9       10      11      12      13      14      15      16
1        7       11      10      12      8       15      7       1       4       8       8       6       10      11      9       13
2        9       13      12      19      13      21      14      8       4       10      8       4       6       7       3       7
3        8       6       7       1       6       11      12      11      17      20      20      18      22      23      17      23
;

nonnegative variables
x(p, w, r) amount (in thousands) transported from plant p to warehouse w to retail store r
;

variable
z
;

equations
objective
plant_const
*warehouse_capacity
retail_const
;

objective.. z =e= sum((p, w, r), (t_p2w(p, w) + t_w2r(w, r)) * x(p, w, r));
*warehouse_capacity(w).. sum((p, r), x(p, w, r)) =l= c;
plant_const(p).. sum((w, r), x(p, w, r)) =l= s(p);
retail_const(r).. sum((p, w), x(p, w, r)) =g= d(r);

model transshipment/all/;
solve transshipment using LP minimizing z;
