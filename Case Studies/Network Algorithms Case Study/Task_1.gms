set
i   nodes /1*20/
;

parameter
M big number /9223372036854775807/
;

alias (i, j);

table t(i,j) time in minutes from node i to node j
          1         2         3         4         5         6         7         8         9         10        11        12        13        14        15        16        17        18        19        20
1         0         5         14        10        [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]
2         5         0         12        [M]       13        9         [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]
3         14        12        0         3         [M]       8         11        [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]
4         10        [M]       3         0         [M]       15        7         [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]
5         [M]       13        16        [M]       0         17        [M]       6         14        [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]
6         [M]       9         8         15        17        0         4         19        7         18        [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]
7         [M]       [M]       11        6         [M]       4         0         [M]       19        11        [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]
8         [M]       [M]       [M]       [M]       6         19        [M]       0         18        20        15        10        [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]
9         [M]       [M]       [M]       [M]       14        7         19        18        0         3         12        5         13        [M]       [M]       [M]       [M]       [M]       [M]       [M]
10        [M]       [M]       [M]       [M]       [M]       18        11        20        3         0         [M]       8         17        [M]       [M]       [M]       [M]       [M]       [M]       [M]
11        [M]       [M]       [M]       [M]       [M]       [M]       [M]       15        12        [M]       0         13        [M]       9         15        20        [M]       [M]       [M]       [M]
12        [M]       [M]       [M]       [M]       [M]       [M]       [M]       10        5         8         13        0         16        17        3         4         [M]       [M]       [M]       [M]
13        [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       13        17        [M]       16        0         [M]       7         9         [M]       [M]       [M]       [M]
14        [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       9         17        [M]       0         4         [M]       7         12        [M]       [M]
15        [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       15        3         7         4         0         18        9         16        12        10
16        [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       20        4         9         [M]       18        0         14        5         [M]       [M]
17        [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       7         9         14        0         18        11        [M]
18        [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       12        16        5         18        0         7         8
19        [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       11        [M]       11        7         0         6
20        [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       [M]       10        [M]       [M]       8         6         0
;

nonnegative Variable  x(i,j);
Variable z;

Equations
objective
source_node
other_nodes
sink_node
;

objective..                                   z =e= sum((i,j),t(i,j)*x(i,j));
source_node(i)$(ord(i)=1)..                   sum(j, x(i, j)) - sum(j, x(j, i))  =e= 1;
other_nodes(i)$(ord(i)>1 and ord(i)<20)..     sum(j, x(i, j)) - sum(j, x(j, i))  =e= 0;
sink_node(i)$(ord(i)=20)..                    sum(j, x(i, j)) - sum(j, x(j, i))  =e= -1;

model shortestroute/all/;
solve shortestroute using lp minimizing z;
display t;
