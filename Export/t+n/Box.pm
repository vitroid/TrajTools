# -*- perl -*-
package Box;

use strict;

BEGIN{
    use Exporter ();
    use vars qw(@ISA @EXPORT @EXPORT_OK);
    
    @ISA       = qw(Exporter);
    @EXPORT    = qw(pbcfunc);
    @EXPORT_OK = qw();
}

use vars @EXPORT_OK;


sub new{
    my ( $package, $bx, $by, $bz ) = @_;
    my $self = {
	size => [ $bx, $by, $bz ]
	};
    bless $self, $package;
}


sub pbcfunc{
    my $self = shift;
    my($x,$y,$z)=@_;
    my($x0,$y0,$z0)=($x,$y,$z);
    my( $bx, $by, $bz ) = @{$self->{size}};
    my( $bxh, $byh, $bzh ) = ( $bx/2, $by/2, $bz/2 );
    while($x<-$bxh){$x+=$bx;}
    while($bxh<=$x){$x-=$bx;}
    while($y<-$byh){$y+=$by;}
    while($byh<=$y){$y-=$by;}
    while($z<-$bzh){$z+=$bz;}
    while($bzh<=$z){$z-=$bz;}
    ($x,$y,$z,$x0-$x,$y0-$y,$z0-$z);
}

1;
