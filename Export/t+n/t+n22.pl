#!/usr/bin/env perl

#
#着色とレイヤ処理の部分をモジュール化する。モジュール名は引数で渡す。
#ということで、オプション類は一旦大半を省く。
#
use Cwd 'abs_path';
#
#着色とレイヤ処理の部分をモジュール化する。モジュール名は引数で渡す。
#ということで、オプション類は一旦大半を省く。
#
BEGIN{
    my $path = abs_path($0);
    $path=~ s!/[^/]*$!!;
    #print $path, "\n";
    push(@INC,$path)
}

use strict;
#use Tip4p;
use Box;
use main;

sub usage{
    print STDERR <<EOD;
usage: $0 [-l hb.ngph][-n] < trajfile.nx4a 
    trajfile: file containing \@NX3A or \@NX4A type data.
Options:
    -nc Module:     Specify NodeColor module (NodeColorQ6P6 etc.)
    -nl Module:     Specify NodeLayer module (NodeLayerNDLT etc.)
    -bc Module:     Specify BondColor module (BondColorQ6P6 etc.)
    -bl Module:     Specify BondLayer module (BondLayerNDLT etc.)
    -pp Module:     Specify PostProcess module (BondDiff etc.)
    -o  Module:     Specify output module (OutputYaplot, OutputPovray, etc.)
    -O  x,y,z :     Give offset to input data.
    -n        :     Show node labels.
EOD
    exit 1;
}

my $bondlayer;
my $bondcolor;
my $nodelayer;
my $nodecolor;
my @postprocess;
my $output;
my $num=0;
my $offsetx;
my $offsety;
my $offsetz;

while ( 1 ){
    $_=shift(@ARGV) || last;
    if ( $_ eq "-bl" ){
	print STDERR "MAIN:$_\n";
	#
	#layer module
	#
	my $module = shift @ARGV;
	require "$module.pm";
	$bondlayer = $module->new( \@ARGV );
    }elsif ( $_ eq "-bc" ){
	print STDERR "MAIN:$_\n";
	#
	#bondcolor module
	#
	my $module = shift @ARGV;
	require "$module.pm";
	$bondcolor = $module->new( \@ARGV );
    }elsif ( $_ eq "-nc" ){
	print STDERR "MAIN:$_\n";
	#
	#nodecolor module
	#
	my $module = shift @ARGV;
	require "$module.pm";
	$nodecolor = $module->new( \@ARGV );
    }elsif ( $_ eq "-nl" ){
	print STDERR "MAIN:$_\n";
	#
	#nodelayer module
	#
	my $module = shift @ARGV;
	require "$module.pm";
	$nodelayer = $module->new( \@ARGV );
    }elsif ( $_ eq "-pp" ){
	print STDERR "MAIN:$_\n";
	#
	#postprocess module
	#
	my $module = shift @ARGV;
	require "$module.pm";
	push @postprocess, $module->new( \@ARGV );
    }elsif ( $_ eq "-o" ){
	print STDERR "MAIN:$_\n";
	#
	#output module
	#
	my $module = shift @ARGV;
	require "$module.pm";
	$output = $module->new( \@ARGV );
    }elsif ( $_ eq "-n" ){
	print STDERR "MAIN:$_\n";
	$num ++;
    }elsif ( $_ eq "-O" ){
	print STDERR "MAIN:$_\n";
	$_=shift;
	($offsetx, $offsety,$offsetz) = split(/[, ]/,$_);
    }else{
	print STDERR "UNKNOWN OPTIONS: MAIN:$_\n";
    }
}



if ( ! defined $bondlayer ){
    use StdLayer;
    $bondlayer = StdLayer->new( 1 );
}
if ( ! defined $bondcolor ){
    use StdColor;
    $bondcolor=StdColor->new( 4 );
}
if ( ! defined $nodelayer ) {
    use StdLayer;
    $nodelayer=StdLayer->new( 2 );
}
if ( ! defined $nodecolor ){
    use StdColor;
    $nodecolor=StdColor->new( 2 );
}
if ( ! defined $output ){
    use OutputYaplot;
    $output=OutputYaplot->new;
}


my $vars = {
    nodelayer => $nodelayer,
    nodecolor => $nodecolor,
    bondlayer => $bondlayer,
    bondcolor => $bondcolor,
    postprocess => \@postprocess,
    output    => $output,
    num       => $num,
    offsetx   => $offsetx,
    offsety   => $offsety,
    offsetz   => $offsetz,
};

my $main = main->new( $vars );
$main->loop();
