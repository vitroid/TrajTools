#!/usr/bin/env perl

#
#Show polyheral fragments
#
#動径分布関数出力用のモード(coverageに比例して点を重ね打ちする)を追加する。
#

use strict;

sub usage{
    die "usage: $0 [-d][-0] ringlist.rngs coord.nx4a < polyhedra.rset\n";
}

sub rint{
  my ( $x ) = @_;
  my $i=0;
  while ( 0.5 <= $x ){
    $i++;
    $x--;
  }
  while ( $x < -0.5 ){
    $i--;
    $x++;
  }
  $i;
}

my $dup="";
my $translate = 0;
while ( $ARGV[0] =~ /^-/ ){
    my $opt = shift;
    if ( $opt eq "-0" ){
	#
	#translate half of the box
	#
	$translate = 1;
    }
    elsif ( $opt eq "-d" ){
	$dup = 1;
    }
    else{
	usage();
    }
}

my $rngs = shift || usage();
my $coord = shift || usage();
open RNGS, "<$rngs";
open COORD, "<$coord" || die "Cannot open $coord.\n";

while(<STDIN>){
    if (/^\@RSET/ ){
	#
	#Read coordinates
	#
	my ( $bx, $by, $bz );
	my @coord;
	while(<COORD>){
	    if ( /^\@BOX3/ ){
		print $_;
		$_ = <COORD>;
		print $_;
		chomp;
		($bx, $by,$bz ) = split;
	    }
	    elsif( /^\@NX4A/ || /^\@AR3A/ ){
		my $n = <COORD>;
		foreach my $i ( 0.. $n-1 ){
		    $_ = <COORD>;
		    chomp;
		    my ( $x,$y,$z) = split;
		    if ( $translate ){
		      $x -= $bx / 2;
		      $y -= $by / 2;
		      $z -= $bz / 2;
		    }
		    if ( $bx ){
			$x -= rint($x/$bx)*$bx;
			$y -= rint($y/$by)*$by;
			$z -= rint($z/$bz)*$bz;
		    }
		    $coord[ $i ] = [ $x,$y,$z ];
		}
		last;
	    }
	}

	#
	#Read ring list
	#
	my @rngs;
	while(<RNGS>){
	    if ( /^\@RNGS/ ){
		my $n = <RNGS>;
		while(<RNGS>){
		    chomp;
		    split;
		    last if $_[0] == 0;
		    shift @_;
		    push @rngs, [ @_ ];
		}
		last;
	    }
	}

	#
	#Read polyhedra (ring sets)
	#
	my $nrings = <STDIN>;
	die "Inconsistency in num of rings.\n" if ( $nrings != $#rngs + 1 );
	my @lines;
	while(<STDIN>){
	    chomp;
	    my @rings = split;
	    last if $rings[0] == 0;
	    shift @rings;

	    #
	    #Extract nodes used by a polyhedron
	    #
	    my %members;
	    foreach my $ring ( @rings ){
		foreach my $node ( @{$rngs[$ring]} ){
		    $members{$node} ++;
		}
	    }
	    my @mems = keys %members;

	    my @rel;
	    my @sum;
	    my $first = $mems[0];
	    my $coverage = 0;
	    foreach my $member ( @mems ){
		if ( $members{$member} == 3 ){
		    $coverage ++;
		}
		#
		#Get the coordinates of nodes relative to the first node.
		#
		my $dx = $coord[$member][0] - $coord[$first][0];
		my $dy = $coord[$member][1] - $coord[$first][1];
		my $dz = $coord[$member][2] - $coord[$first][2];
		if ( $bx ){
		    $dx -= rint( $dx / $bx ) * $bx;
		    $dy -= rint( $dy / $by ) * $by;
		    $dz -= rint( $dz / $bz ) * $bz;
		}
		$rel[$member][0] = $dx;
		$rel[$member][1] = $dy;
		$rel[$member][2] = $dz;
		$sum[0] += $rel[$member][0];
		$sum[1] += $rel[$member][1];
		$sum[2] += $rel[$member][2];
	    }
	    my $m = $#mems + 1;
	    #
	    #Get the center-of-mass relative to the first node.
	    #
	    $sum[0] /= $m;
	    $sum[1] /= $m;
	    $sum[2] /= $m;
	    my $rep = 1;
	    if ( $dup ){
		$rep = $coverage / 2;
	    }
	    for(my $i=0; $i<$rep; $i++ ){
		push @lines, join( " ",
				   $coord[$first][0] + $sum[0],
				   $coord[$first][1] + $sum[1],
				   $coord[$first][2] + $sum[2] ) . "\n";
	    }
	}
	print "\@AR3A\n" , $#lines+1, "\n";
	print join( "", @lines );
    }
}



