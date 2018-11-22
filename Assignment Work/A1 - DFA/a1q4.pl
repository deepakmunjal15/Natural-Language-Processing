#!/usr/bin/perl
use warnings;
use strict;

my $r;
while ($r = <>) {
while ($r =~ /\<h(\d+)(\s+.*?)?>(.*?)<\/h(\d+)(\s+.*?)?>/ig) {
my $final = "<H$1>$3</H$4>";
print "$final\n";
}
}