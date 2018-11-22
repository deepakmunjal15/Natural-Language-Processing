#!/usr/bin/perl
# Letter frequencies

#fill in the blanks _______________
#the required output: letters of the input text 
#with their frequencies and normalized frequencies 
#ordered from the most frequent to the least frequent

use warnings;
use strict;

my %f=();
my $tot=0;


while (<>) {
    while (/[a-zA-Z]/) {
        my $l = $&; 
        $_ = $';
        $f{lc $l} += 1; 
        $tot ++;
    }
}


#another way to do this - using the modifier /g for regex match
#while (<>) {
#    foreach my $let (/[a-zA-Z]/g) {              
#         $f{lc $let} += 1;                                     
#         $tot ++;                                  
#     }
#}


for (sort { $f{$b} <=> $f{$a} } keys %f) {
	print sprintf("%6d %.4lf %s\n",$f{$_}, $f{$_}/$tot, $_);
}
