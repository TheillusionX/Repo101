sets
i events /1*11/
;

parameter
M big number /9223372036854775807/
;

alias (i, j);

table D(i,j) Duration of activity between events i and j
      1    2    3    4    5     6    7    8    9   10   11
1   0.0  9.0  5.0  [M]  [M]   [M]  [M]  [M]  [M]  [M]  [M]
2   [M]  0.0  0.0  [M]  [M]   [M]  [M]  [M]  [M]  [M]  [M]
3   [M]  [M]  0.0  3.0  [M]   [M]  [M]  [M]  [M]  [M]  [M]
4   [M]  [M]  [M]  0.0  6.0  12.0  [M]  7.0  [M]  [M]  [M]
5   [M]  [M]  [M]  [M]  0.0   [M]  5.0  [M]  [M]  [M]  [M]
6   [M]  [M]  [M]  [M]  [M]   0.0  [M]  0.0  [M]  [M]  [M]
7   [M]  [M]  [M]  [M]  [M]   [M]  0.0  [M]  8.0  [M]  [M]
8   [M]  [M]  [M]  [M]  [M]   [M]  [M]  0.0  4.0  [M]  [M]
9   [M]  [M]  [M]  [M]  [M]   [M]  [M]  [M]  0.0  5.0  [M]
10  [M]  [M]  [M]  [M]  [M]   [M]  [M]  [M]  [M]  0.0  4.0
11  [M]  [M]  [M]  [M]  [M]   [M]  [M]  [M]  [M]  [M]  0.0
;

variables
t(i)
z;

equations
objective
nodes
initial_t
;

objective.. z =e= t("11") - t("1");
nodes(i, j)$(D(i,j) < M).. t(j) - t(i) =g= D(i, j);
initial_t.. t("1") =e= 0

model project/all/;
solve project using LP minimizing z;
