#! /usr/bin/env perl
use strict;
use warnings;
use Data::Dumper;

my $in_or_out = shift || 'out';
my $interface = shift;

my $ms1 = uptime();
my $bytesCount1 = getTraffic( $in_or_out, $interface );
sleep 4;
my $ms2 = uptime();
my $bytesCount2 = getTraffic( $in_or_out, $interface );
sleep 4;
my $ms3 = uptime();
my $bytesCount3 = getTraffic( $in_or_out, $interface );

my $bandwidth;
if ( $bytesCount3 < $bytesCount1 ){
die "$interface 锟缴硷拷锟斤拷锟斤拷锟斤拷锟斤拷荩锟杰n";
}
if ( $bytesCount1 <= $bytesCount2 && $bytesCount2 <= $bytesCount3 ){
$bandwidth = ( $bytesCount2 - $bytesCount1 ) * 8 / 1000 / ($ms2-$ms1);
}
else{
$bandwidth = ( $bytesCount3 - $bytesCount1 ) * 8 / 1000 / ($ms3-$ms1);
}

print int($bandwidth), "\n";

exit 0;

##########################################

sub getTraffic {
my $in_or_out = shift;
my $interface = shift;
my $bytesCount = 0;

open my $fh, '/proc/net/dev' or return $bytesCount;
<$fh>; <$fh>;       # skip header

my %traffic;
while(<$fh>){
my @F = split /(?:\s|:)+/;
if ( $in_or_out eq 'in' ){
$traffic{$F[1]} = $F[2];
}
else{
$traffic{$F[1]} = $F[10];
}
}

if (not defined $interface) {
if (exists $traffic{bond0}) {
$interface = "bond0";
}
else {
$interface = "eth1";
}
}

if ($interface eq "bond0") {
if (open(my $fp, "<", "/proc/net/bonding/bond0")) {
my @slaves = grep { /^Slave Interface: (\S+)/ and $_ = $1 } <$fp>;
close $fp;
$traffic{$interface} = 0;
foreach my $slave (@slaves) {
$traffic{$interface} += $traffic{$slave};
}
}
}

$bytesCount = $traffic{$interface};
return $bytesCount;
}

sub uptime {
open my $fh, '/proc/uptime' or return 0;
my $line = <$fh>;
my $uptime = (split /\s+/, $line)[0];
$uptime *= 1000;
return $uptime;
}
