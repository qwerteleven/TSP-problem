include "globals.mzn";
int : node_count;

set of int: nodes = 1..node_count;
array [nodes] of var nodes: orden;
array [nodes, 1..2] of float: map;


constraint forall(i,j in nodes where j > i)(orden[i] != orden[j]);
constraint forall(i,j in nodes where j > i)(orden[j] != orden[i]);
constraint alldifferent([orden[i] | i in nodes]);
%constraint circuit([orden[i] | i in nodes]);

%constraint forall(i,k in 1..node_count where k > i)(orden[i] = i + arg_min([abs(map[orden[i],1] - map[orden[j],1]) + abs(map[orden[i],2] - map[orden[j],2]) | j in k..node_count]));


constraint orden[1] = 1;

var float: regreso = abs(map[orden[node_count],1] - map[orden[1],1]) + abs(map[orden[node_count],2] - map[orden[1],2]);

var float: recorrido = sum(i in 1..node_count-1)(abs(map[orden[i],1] - map[orden[i+1],1]) + abs(map[orden[i],2] - map[orden[i+1],2])) + regreso;

%solve minimize recorrido;
%solve satisfy;
solve :: int_search(orden, first_fail, indomain_min, complete) minimize recorrido;
