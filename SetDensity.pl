#!/usr/bin/env perl

#水の座標を標準入力から読み、指定された密度に変換する。

use strict;
die "usage: $0 [-z] density [molweight]\n" if $#ARGV<0;
my $na=6.0221367e23;
my $specdens=shift;
my $expandz;
if ( $specdens eq '-z' ){
    $expandz ++;
    $specdens = shift;
}

my $mass;
if($ARGV[0]){
    $mass=$ARGV[0];
}else{
    $mass=18;
}
my ($bx,$by,$bz);
while(<STDIN>){
    if(/^\s*\@BOX3/){
	$_=<STDIN>;
	chomp;
	($bx,$by,$bz)=split;
    }elsif(/^\@BXLA/){
	$_=<STDIN>;
	chomp;
	$bx=$by=$bz=$_;
    }elsif(/^\@NX[34]A/ || /^\@WTG[36]/ || /^\@AR3A/ ){
	my $type=$_;
	my $n=<STDIN>;
	my $density=$n*$mass/($bx*$by*$bz*1e-24*$na);
	print STDERR "Original Density: $density\n";
	my $scalex;
	my $scaley;
	my $scalez;
	if ( $expandz ){
	    $scalez= $density/$specdens;
	    $scalex = $scaley = 1;
	}
	else{
	    $scalez=exp((1.0/3.0)*log($density/$specdens));
	    $scalex = $scaley = $scalez;
	}
	$bx*=$scalex;
	$by*=$scaley;
	$bz*=$scalez;
	print "\@BOX3\n";
	print "$bx $by $bz\n";
	print $type;
	print $n;
	for(my $i=0;$i<$n;$i++){
	    $_=<STDIN>;
	    chomp;
	    @_ = split;
	    $_[0]*=$scalex;
	    $_[1]*=$scaley;
	    $_[2]*=$scalez;
	    print join(" ",@_),"\n";
	}
    }
    else{
	print;
    }
}
