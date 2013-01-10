#!/usr/bin/env perl

package ogi2;

use strict;

sub new{
    my $package = shift;
    my $self;
    foreach my $i ( 0 .. 9999 ){
	$self->{ginfo}[$i] = -1;
    }
    bless $self, $package;
}

sub query{
    my ( $self, $id ) = @_;
    my $j;
    while(1){
	$j = $self->{ginfo}[$id];
	if ( $j < 0 ){
	    my $size = -$j;
	    return ($id, $size);
	}
	$id = $j;
    }
    exit 1;
}


sub set{
    my ( $self, $id, $group, $newginfo ) = @_;
    while(1){
	my $j = $self->{ginfo}[$id];
	if ( $j < 0 ){
	    $self->{ginfo}[$id] = $newginfo;
	    return;
	}
	$self->{ginfo}[$id] = $group;
	$id = $j;
    }
    exit 2;
}



sub add{
    my ( $self, $i, $j ) = @_;

    my ( $ig, $im ) = $self->query( $i );
    my ( $jg, $jm ) = $self->query( $j );
    if ( $ig != $jg ){
	$self->set( $i, $ig, -($im+$jm) );
	$self->set( $j, $ig, $ig );
    }
}

1;
