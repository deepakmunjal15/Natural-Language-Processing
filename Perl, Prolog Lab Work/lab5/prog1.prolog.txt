hare(roland).
turtle(franklin).
faster(X,Y) :- hare(X), turtle(Y).

busy(X,D) :- taking_course(X,Y), haslecture(Y,D).
taking_course(joe,nlp).
haslecture(nlp,friday).

person(john,public,'123-456').

member(X, [X|_]).
member(X, [_|L]) :- member(X,L).
