# -*- perl -*-
package RigidWater;
use strict;
use Tip4p;
#Single molecule.

sub new{
    my ( $package, %argref ) = @_;
    my $self = {
	output => $argref{output},
	box    => $argref{box},
	shownum=> $argref{shownum},
	order  => $argref{order}
	};
    bless $self, $package;
}


sub config{
    my $self = shift;
    my ( $x, $y, $z, $a, $b, $c, $d ) = @_;
    if( $self->{box} ){
	($x,$y,$z)=$self->{box}->pbcfunc( $x, $y, $z );
    }
    if ( $d ne "" ){
	$self->{coord} = [ 0, 0, 0, tip4pnx4a( $a,$b,$c,$d ) ];
    }
    else{
	$self->{coord} = [ 0, 0, 0, tip4pconf( $a,$b,$c ) ];
    }
    for(my $i=0; $i<12; $i+=3){
	$self->{coord}[$i+0] += $x;
	$self->{coord}[$i+1] += $y;
	$self->{coord}[$i+2] += $z;
    }
}


sub GetPosition{
    my ($self) = @_;
    return @{$self->{coord}};
}


    
sub draw{
    my $self = shift;
    my $output = $self->{output};
    my @ra = @{$self->{coord}};
    $output->ohbond($ra[3],$ra[4],$ra[5],$ra[6],$ra[7],$ra[8]);
    $output->ohbond($ra[3],$ra[4],$ra[5],$ra[9],$ra[10],$ra[11]);
    $output->hydrogen($ra[6],$ra[7],$ra[8]);
    $output->hydrogen($ra[9],$ra[10],$ra[11]);
    $output->oxygen($ra[3],$ra[4],$ra[5]);
    if( $self->{shownum} ){
	$output->molnum($ra[3],$ra[4],$ra[5],$self->{order} );
    }
}



sub drawbond{
    my $self = shift;
    my $another = shift;
    if ( ref $another ne ref $another ){
	print STDERR ref $another;
	exit;
    }
    my ($xi,$yi,$zi)=@{$self->{coord}};
    my ($xj,$yj,$zj)=@{$another->{coord}};
    my $dx = $xi-$xj;
    my $dy = $yi-$yj;
    my $dz = $zi-$zj;
    if( $self->{box} ){
	($dx,$dy,$dz)=$self->{box}->pbcfunc($dx,$dy,$dz);
    }
    my $output = $self->{output};
    $output->hbond($xi,$yi,$zi,$xi-$dx,$yi-$dy,$zi-$dz);
}

1;
