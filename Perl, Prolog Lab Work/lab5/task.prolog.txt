is_child(john,mary).
is_child(ann,john).
is_child(tom,john).
is_grandchild(X,Z) :- is_child(X,Y), is_child(Y,Z).
