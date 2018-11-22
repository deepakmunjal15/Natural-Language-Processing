s(s(Tn,Tv)) --> np(Tn,A), vp(Tv,A).
np(np(Td,Tn),A) --> d(Td), n(Tn,A).
d(d(the)) --> [the].
n(n(Np1),p1) --> [Np1],
{ atom_concat(Nsg, 's', Np1), n(_,sg,[Nsg],[]) }.
n(n(X),sg) --> [X], 
{ member(X, [dog, cat]) }.
n(n(X),sg) --> [X], 
{ member(X, [turtle, rabbit]) }.
vp(vp(Vsg),sg) --> [Vsg],
{ atom_concat(Vp1, 's', Vsg), vp(_,p1,[Vp1],[]) }.
vp(vp(X),p1) --> [X], 
{ member(X, [run, walk]) }.
vp(vp(X),p1) --> [X], 
{ member(X, [swim, crawl]) }.

member(X, [X|_]).
member(X, [_|L]) :- member(X, L).
