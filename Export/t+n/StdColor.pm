#!/usr/bin/env perl
package StdColor;

use strict;
use FileHandle;

#指定されたファイルから、指定されたタグのデータを読みこむ。
#問いあわせがあれば、あるノードの色番号を返す

sub new{
    my $package = shift;
    my $self = {
	value => shift
    };
    bless $self, $package;
}

sub done{
    my ( $self ) = @_;
}

sub load{
    my ( $self ) = @_;
}

sub value{
    my ( $self, $order ) = @_;
    return $self->{value};
}

sub setpalette{
    my ( $self ) = @_;
}



1;
