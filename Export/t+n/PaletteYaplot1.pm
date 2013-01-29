package PaletteYaplot1;
use strict;


sub new{
    my ( $package ) = @_;
    my $self = {};
    bless $self, $package;
}

sub colorsetting{
    my ($self)=@_;
    $self->{max} = 50;
    print "@ 1 30 30 30\n";
    for(my $i=3;$i<50;$i++){
	my $j=$i*15;
	my $k=$i*15;
	if($j>255){$j=255;}
	if($k>155){$k=155;}
	print "@ $i $k $j $j\n";
    }
}

1;
