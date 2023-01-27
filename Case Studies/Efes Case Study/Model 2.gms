Sets
i /"Afyon", "Konya", "Import (Izmir)"/ set of malt plant i
j /"Istanbul", "Ankara", "Izmir", "Sakarya", "Adana"/ set of brewer j
k /"Istanbul", "Izmir", "Antalya", "Bursa", "Kayseri", "Export (Izmir)"/ set of distribution center k
y /"Year 1" * "Year 20"/ set of year y
;

alias(y, t);

parameters
t_m(i, j) cost of shipping malt (in million $ per 1000 tons) from malt plant i to brewery j
C_m(i) capacity of malt plant i (in thousand tons per year)

t_b(j, k) cost of shipping beer (in million $ per million liters) from brewery j to distribution center k
C_b(j) capacity of brewery j (in million liters per year)
N_b(j) new capacity after building brewery j (in million liters per year)
E_b(j) additional capacity after expansion of new brewery j (in million liters per year)

D(k, y) demand of distribution center k (in million liters per year) in year y

CN_Nom(j) the nominal cost of opening brewery site j in year 1
CE_Nom(j) the nominal cost of expanding brewery site j in year 1

CN(j, y) the NPV of opening new brewery site j in year y at 10% discount rate
CE(j, y) the NPV of expanding new brewery site j in year y at 10% discount rate

Y_m(i) yield of malt from malt plant i
/"Afyon" 8.333,
 "Konya" 8.333,
 "Import (Izmir)" 9.091
/
;

*$CALL GDXXRW "D:\METU\METU 4th Semester\IE252\Homework\Case Study 2\IE252 Case Study 2 Parameters.xls" output = "Params2.gdx" par=t_m rng=data!B7 cDim=1 rDim=1 par=C_m rng=data!K5 cDim=0 rDim=1 par=t_b rng=data!B16:H21 par=C_b rng=data!P6:Q8 cDim=0 rDim=1 par=D rng=data!K23:P29 cDim=1 rDim=1 par=N_b rng=data!P9:Q12 cDim=0 rDim=1 par=E_b rng=data!P9:R12 cDim=0 rDim=1 ignoreColumns=Q par=CN_Nom rng=data!B28:C31 cDim=0 rDim=1 par=CE_Nom rng=data!B29:D31 ignoreColumns=C cDim=0 rDim=1 
$GDXin Params2.gdx
$load t_m, C_m, t_b, C_b, N_b, E_b, D, CN_Nom, CE_Nom
$GDXin


CN(j, y)$(ord(y) <= 3) = CN_Nom(j) * 1/(1.1 ** (ord(y) - 1));
CE(j, y)$(ord(y) <= 3) = CE_Nom(j) * 1/(1.1 ** (ord(y) - 1));

D(k, y)$(ord(y) > 3) = D(k, "Year 3");

display t_m, C_m, t_b, C_b, N_b, E_b, D, CN_Nom, CE_Nom, CN, CE;

nonnegative variables
m(i, j, y) malt (in thousand tons) transported between malt plant i to brewery j in year y
b(j, k, y) million liters of beer transported between brewery j to distribution center k in year y
;

binary variables
o(j, y) Equal to 1 if potential brewery site j will open in year y and 0 otherwise
e(j, y) Equal to 1 if potential brewery site j is expanded in year y and 0 otherwise
;

variables
z objective function
;

equations
objective
supply
brewery_capacity
malt_yield
only_open_once
only_expand_opened_site
only_expand_once
demand
old_breweries_are_built
old_breweries_dont_expand
dont_open_after_three_years
dont_expand_after_three_years
;

objective.. z =e= sum((i, j, y), t_m(i, j) * m(i, j, y)) + sum((j, k, y), t_b(j, k) * b(j, k, y)) + sum((j, y), CN(j, y) * o(j, y)) + sum((j, y), CE(j, y) * e(j, y));

supply(i, y).. sum(j, m(i, j, y)) =l= C_m(i);

*brewery_capacity(j, y).. sum(i, m(i, j, y)) =l= C_b(j) + sum(t$(ord(t) <= ord(y)), N_b(j) * o(j, t) + E_b(j) * e(j, t));
brewery_capacity(j, y).. sum(k, b(j, k, y)) =l= C_b(j) + sum(t$(ord(t) <= ord(y)), N_b(j) * o(j, t) + E_b(j) * e(j, t));

malt_yield(j, y).. sum(i, Y_m(i) * m(i, j, y)) =e= sum(k, b(j, k, y));

only_open_once(j).. sum(y, o(j, y)) =l= 1;

only_expand_opened_site(j, y).. e(j, y) =l= sum(t$(ord(t) <= ord(y)), o(j, t));

only_expand_once(j).. sum(y, e(j, y)) =l= 1;

demand(k, y).. sum(j, b(j, k, y)) =g= D(k, y);

old_breweries_are_built(j, y)$(ord(j) <= 2).. o(j, y) =e= 0;

old_breweries_dont_expand(j, y)$(ord(j) <= 2).. e(j, y) =e= 0;

dont_open_after_three_years(j, y)$(ord(y) > 3).. o(j, y) =e= 0;

dont_expand_after_three_years(j, y)$(ord(y) > 3).. e(j, y) =e= 0

*option LimRow = 100;

model transshipopenment /all/;
solve transshipopenment using MIP minimizing z;







