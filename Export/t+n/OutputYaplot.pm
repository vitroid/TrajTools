# -*- perl -*-

package OutputYaplot;
use strict;

sub new{
    my ( $package, $argref ) = @_;
    my $self = { 
	rep => 1,
    };
    while( 1 ){
	if ( $argref->[0] eq "-p" ){
	    $_=shift(@{$argref});
	    print STDERR "$package:$_\n";
	    #
	    #palette module
	    #
	    my $module = shift @{$argref};
	    require "$module.pm";
	    $self->{palette} = $module->new( $argref );
	}
	elsif ( $argref->[0] eq "-r" ){
	    $_=shift(@{$argref});
	    print STDERR "$package:$_\n";
	    $self->{rep} = shift(@{$argref}) || usage();
	}
	else{
	    last;
	}
    }
    if ( ! defined $self->{palette} ){
	use PaletteYaplot1;
	print STDERR "$package:use default palette\n";
	$self->{palette}=PaletteYaplot1->new;
    }
    bless $self, $package;
}



sub usage{
    print STDERR <<EOD;
(Module for t+n2.pl)
usage: $0 [-p Module][-r nrep]
Options:
    -r nrep:       Repeat drawing image cells nrep times.
    -p Module:     Specify Palette module (PalettePovray1 etc.)
EOD
    exit 1;
}



sub SetBox{
    my $self = shift;
    $self->{box} = shift;
}


sub repeat{
    my ( $self, $method, @x ) = @_;
    if ( 1 < $self->{rep} && defined $self->{box} ){
	my $rep = $self->{rep};
	my ( $bx, $by, $bz )    = @{$self->{box}->{size}};
	my ( $bxh, $byh, $bzh ) = ( $bx/2, $by/2, $bz/2 );
	my($ix,$iy,$iz,$xx,$yy,$zz,$i,$n);
	for($ix=0;$ix<$rep;$ix++){
	    $xx=$bx*$ix-$bxh*($rep-1);
	    for($iy=0;$iy<$rep;$iy++){
		$yy=$by*$iy-$byh*($rep-1);
		for($iz=0;$iz<$rep;$iz++){
		    $zz=$bz*$iz-$bzh*($rep-1);
		    my @y;
		    for(my $i=0; $i<= ($#x-2); $i+=3 ){
			$y[$i+0] = $x[$i+0] + $xx;
			$y[$i+1] = $x[$i+1] + $yy;
			$y[$i+2] = $x[$i+2] + $zz;
		    }
		    $self->$method( @y );
		}
	    }
	}
    }
    else{
	$self->$method( @x );
    }
}


sub printdefect1{
    my($self, $x, $y, $z)=@_;
    print "r 0.2\n";
    printf "o %7.3f %7.3f %7.3f\n" ,$x,$y,$z;
}


sub printdefect{
    my $self = shift;
    $self->repeat( "printdefect1", @_ );
}


sub ohbond1{
    my($self,$sx,$sy,$sz,$ex,$ey,$ez)=@_;
    #printf "@ 2\nl %7.3f %7.3f %7.3f  %7.3f %7.3f %7.3f\n",$sx,$sy,$sz,$ex,$ey,$ez;
    printf "l %7.3f %7.3f %7.3f  %7.3f %7.3f %7.3f\n",$sx,$sy,$sz,$ex,$ey,$ez;
}



sub ohbond{
    my $self = shift;
    $self->repeat( "ohbond1", @_ );
}


sub trace1{
    my($self,$sx,$sy,$sz,$ex,$ey,$ez)=@_;
    printf "@ 6\nl %7.3f %7.3f %7.3f  %7.3f %7.3f %7.3f\n",$sx,$sy,$sz,$ex,$ey,$ez;
}


sub trace{
    my $self = shift;
    $self->repeat( "trace1", @_ );
}


sub hbond1{
    my($self,$sx,$sy,$sz,$ex,$ey,$ez)=@_;
    printf "l %7.3f %7.3f %7.3f  %7.3f %7.3f %7.3f\n",
    $sx,$sy,$sz,$ex,$ey,$ez;
}


sub hbond{
    my $self = shift;
    $self->repeat( "hbond1", @_ );
}



sub hydrogen1{
    my($self,$x,$y,$z)=@_;
}

sub hydrogen{
    my $self = shift;
    $self->repeat( "hydrogen1", @_ );
}

sub oxygen1{
    my($self,$x,$y,$z)=@_;
}

sub oxygen{
    my $self = shift;
    $self->repeat( "oxygen1", @_ );
}



sub TextLabel{
    my($self,$x,$y,$z,$label)=@_;
    printf "t %7.3f %7.3f %7.3f %d\n",$x,$y,$z,$label;
}


sub molnum1{
    my($self,$x,$y,$z,$num)=@_;
    $self->TextLabel($x,$y,$z,$num);
}



sub molnum{
    my $self = shift;
    $self->repeat( "molnum1", @_ );
}





sub poly1{
    my($self,@coord)=@_;
    my $n = ($#coord+1) / 3;
    print join( " ", "p", $n, @coord ), "\n";
}



sub poly{
    my $self = shift;
    $self->repeat( "poly1", @_ );
}


sub newpage{
    print "\n";
}

sub startpage{
    my $self = shift;
    $self->{palette}->colorsetting( );
}


sub SetLayer{
    my $self=shift;
    print "y $_[0]\n";
}

sub SetPalette{
    my $self=shift;
    my $palette = shift;
    if ( defined $self->{palette}->{max} && $self->{palette}->{max} <= $palette ){
	$palette = $self->{palette}->{max} - 1;
    }
    print "@ $palette\n";
}

1;
