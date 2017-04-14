V(0) :- not(running(c1, 1)), not(running(c2, 1)), not(running(c3, 1)).
V(1) :- running(c1, 1),      not(running(c2, 1)), not(running(c3, 1)).
V(1) :- not(running(c1, 1)), running(c2, 1),      not(running(c3, 1)).
V(1) :- not(running(c1, 1)), not(running(c2, 1)), running(c3, 1).
V(2) :- running(c1, 1),      running(c2, 1),      not(running(c3, 1)).
V(2) :- running(c1, 1),      not(running(c2, 1)), running(c3, 1).
V(2) :- not(running(c1, 1)), running(c2, 1),      running(c3, 1).
V(3) :- running(c1, 1),      running(c2, 1),      running(c3, 1).