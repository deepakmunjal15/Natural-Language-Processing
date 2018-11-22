gcd(A,A,A).
gcd(A,B,G) :- A=\=B, C is min(A,B),
       X is A - B, D is abs(X),
       gcd(C,D,G).
