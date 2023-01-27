sets
c indice of fuel types /stockpile, colombian, russian, scottish, wood_chips/
m indice of months /1*5/
w indice of periods /weekday_peak, weekday_off, weekend_peak, weekend_off/
;

scalar
Hrs "Hours in each period" /12/
L "Amount of MWh produced from each GJoule" /0.278/
SB "Sulfur Bubble limit" /9000/
CO "CO2 emitted from one MWh" /0.8/
E_l "Energy limit of powerplant" /1000/
epsi "Efficiency of powerplant" /0.35/
I "Inventory of stockpiled coal available" /600000/
T_r "Commission rate" /0.975/
T_e "Rate imposed on CO2 emissions" /15/
T_roc "ROC value" /67.5/
;

parameters

pf(c) price of fuel c per tonne
/stockpile 63.84,
 colombian 65.895,
 russian 65.7,
 scottish 63,
 wood_chips 110.655/

v(c) calorific value of fuel c per tonne
/stockpile 25.81,
 colombian 25.12,
 russian 24.50,
 scottish 26.20,
 wood_chips 1.8/

s(c) SO rating of fuel c per tonne
/stockpile 0.0138,
 colombian 0.007,
 russian 0.0035,
 scottish 0.0172,
 wood_chips 0.0001/

table pe(m, w) price of future electricity in period w in month m
         weekday_peak       weekday_off       weekend_peak       weekend_off
1        54                      40.5            50.25                   39.3
2        54.525                  40.5            51.45                   39.45
3        56.475                  42.3            53.475                  41.25
4        57.525                  42.75           53.7                    41.475
5        65.5                    47.55           58.05                   45.15
;

table h(m, w) number of weekdays or weekends (determined by p) in month m
         weekday_peak       weekday_off       weekend_peak       weekend_off
1        22                      22              8                   8
2        21                      21              10                  10
3        23                      23              8                   8
4        22                      22              8                   8
5        21                      21              10                  10
;

nonnegative variables
e(c, m, w) Amount of fuel c used up in month m to sell fuel in period w
;

variable
z total profit
;

equations
objective_function
power_plant_limit
stockpile_entire_period
sulfur_bubble
coal_lead_up
;

objective_function.. z =e= sum( (c,m,w), pe(m,w)*h(m,w)*epsi*L*v(c)*e(c,m,w))
                         + sum( (m,w), T_roc*h(m,w)*epsi*L*v('wood_chips')*e('wood_chips',m,w))
                         - sum( (c,m,w), pf(c)*h(m,w)*e(c,m,w) )
                         - sum( (c,m,w), T_e*CO*h(m,w)*epsi*L*v(c)*e(c,m,w))
                         - sum( (c,m,w), T_r*h(m,w)*epsi*L*v(c)*e(c,m,w));

power_plant_limit(m, w).. sum(c, epsi*L*v(c)*e(c,m,w)) =l= Hrs*E_l;

stockpile_entire_period.. sum((m, w), h(m,w)*e('stockpile', m, w) ) =l= I;

sulfur_bubble.. sum( (c,m,w), s(c)*h(m,w)*e(c,m,w) ) =l= SB;

coal_lead_up(c, m, w)$(ord(c)>1 and ord(c)<5 and ord(m)<4).. e(c, m, w) =e= 0;

model IC/all/;
solve IC using LP maximizing z;
display z.l;
