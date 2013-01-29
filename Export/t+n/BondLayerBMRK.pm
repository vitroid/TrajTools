#!/usr/bin/env perl
package BondLayerBMRK;

use strict;
use FileHandle;

#指定されたファイルから、指定されたタグのデータを読みこむ。
#問いあわせがあれば、あるノードのレイヤを返す

sub new{
    my ( $package, $argref ) = @_;
    my $self = {
	filehandle => FileHandle->new( shift @{$argref} ),
	tag        => shift( @{$argref} )
    };
    bless $self, $package;
}

sub done{
    my ( $self ) = @_;
    FileHandle->close( $self->{filehandle} );
}

sub load{
    my ( $self ) = @_;
    my $fh = $self->{filehandle};
    my $line;
    while( $line = $fh->getline ){
	chomp($line);
	if ( $line eq $self->{tag} ){
	    my $n          = $fh->getline;
	    $self->{ndata} = $n;
	    undef $self->{data};
	    while( $_ = $fh->getline ){
		# 結合しているノード対と、その寿命を読みこむ。
		my ($x, $y, $layer)= split;
		last if  $x < 0;

		$self->{data}{$x}{$y} = $layer + 3;
		$self->{data}{$y}{$x} = $layer + 3;
	    }
	    return;
	}
    }
}

#
#外部から呼ばれ、結合(node1, node2)のlayerを返す関数。
#
sub value{
    my ( $self, $node1, $node2 ) = @_;
    $self->{data}{$node1}{$node2};
}

#
#????平成16年10月20日(水)
#
sub setpalette{
    my ( $self ) = @_;
}

1;
