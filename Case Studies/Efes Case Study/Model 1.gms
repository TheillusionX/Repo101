sets
i /"Afyon", "Konya", "Import (Izmir)"/ set of malt plant i
j /"Istanbul", "Ankara"/ set of brewer j
k /"Istanbul", "Izmir", "Antalya", "Bursa", "Kayseri", "Export (Izmir)"/ set of distribution center k

parameters
t_m(i, j) cost of shipping malt (in million $ per 1000 tons) from malt plant i to brewery j
C_m(i) capacity of malt plant i (in thousand tons per year)

t_b(j, k) cost of shipping beer (in million $ per million liters) from brewery j to distribution center k
C_b(j) capacity of brewery j (in million liters per year)

D(k) demand of distribution center k (in million liters per year)
;

Scalar
Y_d /8.333/ Scalar yield of beer (in million liters) from 1000 tons of domestic malt
Y_i /9.091/ Scalar yield of beer (in million liters) from 1000 tons of imported malt
;

*$CALL GDXXRW "D:\METU\METU 4th Semester\IE252\Homework\Case Study 2\IE252 Case Study 2 Parameters.xls" output = "Params.gdx" par=t_m rng=data!B7 cDim=1 rDim=1 par=C_m rng=data!K5 cDim=0 rDim=1 par=t_b rng=data!B16:H18 par=C_b rng=data!P6 cDim=0 rDim=1 par=D rng=data!K24 cDim=0 rDim=1
$GDXin Params.gdx

$load D, t_m, C_m, t_b, C_b
$GDXin

display t_m, C_m, t_b, C_b, D;

variable
z objective function
;

nonnegative variables
m(i, j) tons (in thousands) of malt transported from malt plant i to brewery j
b(j, k) liters (in millions) of beer transported from brewery j to distribution center k
;

equations
objective
supply
brewery_capacity
yield_of_malt
demand
;

objective.. z =e= sum((i,j), t_m(i, j) * m(i, j)) +
                    sum((j, k), t_b(j,k) * b(j, k));

supply(i).. sum(j, m(i, j)) =l= C_m(i);

brewery_capacity(j).. sum(k, b(j, k)) =l= C_b(j);
*brewery_capacity(j).. sum(i, m(i, j)) =l= C_b(j);

yield_of_malt(j).. Y_d * sum((i)$(ord(i) < 3), m(i, j)) +
                    Y_i * m("Import (Izmir)", j) =e= sum(k, b(j, k));

demand(k).. sum(j, b(j, k)) =g= D(k);

model TRANSPORTATION_MODEL /all/;

solve TRANSPORTATION_MODEL using LP minimizing z;