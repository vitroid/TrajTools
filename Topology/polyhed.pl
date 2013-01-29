#!/usr/bin/env perl
#
#Read list of rings, and look up "polyhedral fragments".
#Here fragment means an undirected graph, which is usually a part of a
# larger network.
#Polyhedral fragment consists of a couple of rings that satisfy:
#1.All the nodes of the fragment must have at least 2 edges.
#2.All the nodes of the fragment must be shared by 2 or 3 rings.
#3.Complexity must be 1, where complexity C is defined as
#  C = S - E + V - 1,
# where S, E, and V are the number of rings, edges, and nodes, respectively.
# This is derived from Euler's formula to evaluate the topological complexity
# of a polyhedron-like graph.
#4.Fragment must not have interior nodes. Interior node is a node inside the
# polyhedral hull but does not belong to the hull itself.
# 
#
#2005-11-24
# -l option is added to avoid slowness :-)
#
#crossingring.pl is available to eliminate entangled rings.
#

use strict;
BEGIN{
  use File::Basename;
  use Cwd 'abs_path';
  push @INC, dirname(abs_path($0));
}


#
#Global vars
#

#
#$Limit specifies the largest size of the rings utilized for fragments.
#
my $MAXRINGSIZE;
my $MAXFRAGSIZE;
my $NOCHECKCOMPO;
my $DEBUG = 0;
while( 0 <= $#ARGV ){
    if ( $ARGV[0] eq "-x" ){
	shift;
	$MAXRINGSIZE = $ARGV[0];
    }
    if ( $ARGV[0] eq "-l" ){
	shift;
	$MAXFRAGSIZE = $ARGV[0];
    }
    elsif ( $ARGV[0] eq "-d" ){
	$DEBUG ++;
    }
    elsif ( $ARGV[0] eq "-n" ){
      #小さなクラスタをフラグメント分割する場合、フラグメントによりクラスタが2分される場合はよくある。それを避けるため。
	$NOCHECKCOMPO ++;
    }
    shift;
}

my @PLACED;
my @RINGSINTHEPOLY;
my @NUMRINGSATTHENODE;
my $NPOLY=0;
my $NUMNODES;
my %EDGES;
my $ORIGINALCOMPO;
#
#When $RSET is non-zero, fragments are output in @RSET format.
#(@RSET is the format for set of rings.)
#
my $RSET = 1;
#
#When $NGPH is non-zero, fragments are output in @NGPH format.
#
my $NGPH = 0;

#
#list rings having the specified 3 successive nodes (center, left, and right)
#
sub attach{
    my ( $nodes, $center, $left, $right, $perimeter ) = @_;

    my $nn = $#{$nodes};
    my @n = @{$nodes};
    #print join(" ", "RING:", @n),"\n";
    #
    #fail safe
    #
    push @n, $n[0];
    my $i;
    for($i=0; $i<= $nn; $i++ ){
	last if ( $n[$i] == $center );
    }
    if ( $n[$i+1] != $right ){
	@n = reverse @{$nodes};
	$i = $nn - $i;
    }
    #
    #rotate and move center to the first element of @n
    #
    @n = (@n[0..$nn],@n[0..$nn])[$i..$i+$nn];
    #print join(" ", "RING>", @n),"\n";

    my @p = @{$perimeter};
    #print join(" ", "PERI:", @p),"\n";
    for($i=0;$i<=$#p;$i++){
	last if $p[$i] == $center;
    }
    @p = (@p,@p)[$i..$i+$#p];
    #print join(" ", "PERI>", @p),"\n";

    #
    #match reversely
    #
    @p = reverse @p;
    @n = reverse @n;
    for( $i=0;$i<=$#n;$i++ ){
	last if $n[$i] != $p[$i];
    }
    @p = reverse( (@p,@p)[$i..$i+$#p] );
    @n = reverse( (@n,@n)[$i..$i+$#n] );

    my @shared;
    while( $n[0] == $p[0] && 0 <= $#n){
	push @shared, shift @n;
	shift @p;
    }
    #print join(" ", "PERI>", @p),"\n";
    my @newperi;
    if ( 0 <= $#p ){
	@newperi =  ( $shared[0], reverse(@n), $shared[$#shared], @p );
    }
    #print join(" ", "NEWP:", @newperi),"\n";
    return @newperi;
}

    
#
#main loop
#
while(<STDIN>){
    #
    #Read ring list from STDIN
    #
    if ( /^\@RNGS/ ){
	#
	#First line contains the number of nodes in the graph.
	#
	$NUMNODES = <STDIN>;
	print "\@FSEP\n";
	#
	#Node list of all rings
	#
	my @rings;
	#
	#All node triplets
	#
	my %node3;
	#
	#All HB pairs
	#
	undef %EDGES;
	while(<STDIN>){
	    chomp;
	    my @nodes = split;
	    last if $nodes[0] <= 0;
	    my $size = shift @nodes;
	    if ( $MAXRINGSIZE && $MAXRINGSIZE < $size ){
		next;
	    }
	    #
	    #register to ring list
	    #
	    push @rings, [ @nodes ];
	    #
	    #register the ring to "node triplets" owner list 
	    #
	    push @nodes,$nodes[0], $nodes[1];
	    for(my $i=0; $i<$size; $i++){
		#
		#Register node triplets.
		#first key is the central node. not the first node of 3 nodes.
		#
		push @{ $node3{$nodes[$i+1]}{$nodes[$i]}{$nodes[$i+2]} }, $#rings;
		push @{ $node3{$nodes[$i+1]}{$nodes[$i+2]}{$nodes[$i]} }, $#rings;
		#
		#Register bonds
		#
		$EDGES{$nodes[$i]}{$nodes[$i+1]} = 1;
		$EDGES{$nodes[$i+1]}{$nodes[$i]} = 1;
	    }
	}
	$ORIGINALCOMPO = components2();
	if ( $RSET ){
	    print "\@RSET\n", $#rings + 1, "\n";
	}
	foreach my $ring ( 0 .. $#rings ){
	    LookupPolyhed( \@rings, \%node3, $ring );
	}
	if ( $RSET ){
	    print "0\n";
	}#
	#
	#read first frame only.
	#
	#exit 0;
    }
}


sub LookupPolyhed{
    my ( $ringlist, $node3, $originring ) = @_;

    #
    #perimeter of the current fragment
    #
    my @perimeter = @{ $ringlist->[$originring] };
    #
    #already placed rings
    #
    $PLACED[$originring] = 1;
    push @RINGSINTHEPOLY, $originring;
    #
    #share number of each node
    #
    foreach my $node ( @perimeter ){
	$NUMRINGSATTHENODE[$node]++;
    }
    #
    #you can start wherever you want.
    #
    my $center = $perimeter[0];
    my $right = $perimeter[1];  #right must be the succ element of center

    foreach my $left ( keys %{ $node3->{$center}{$right} } ){
	ExtendPerimeter( $ringlist, $node3, $originring, \@perimeter, $left, $center, $right );
    }

    $PLACED[$originring] = 0;
    pop @RINGSINTHEPOLY;
    #
    #share number of each node
    #
    foreach my $node ( @perimeter ){
	$NUMRINGSATTHENODE[$node]--;
    }
}



#
#Extend the perimeter of adjacent rings by attaching a new ring on the
# perimeter.
#
sub ExtendPerimeter{
    my ( $ringlist, $node3, $originring, $peri, $left, $center, $right ) = @_;
    my @perimeter = @{$peri};

    #
    #Limit the fragment size.
    #
    if ( $MAXFRAGSIZE && $MAXFRAGSIZE <= $#RINGSINTHEPOLY + 1 ){
	#print STDERR "-";
	return;
    }

    #print "Extension.\n";
    #
    #for each ring owning the triplets.
    #
    foreach my $ring ( @{ $node3->{$center}{$right}{$left} } ){
	#print "$left-$center-$right $originring, $ring\n";
	#
	# origin ring must have the smallest label.
	#
	if ( $originring < $ring ){
	    if ( ! $PLACED[$ring] ){
		my @newperi = attach( $ringlist->[$ring], $center, $left, $right, \@perimeter );
		#
		#mark the ring as used.
		#
		$PLACED[$ring] = 1;
		push @RINGSINTHEPOLY, $ring;
		#
		#Increment the number of rings sharing the node.
		#
		foreach my $node ( @{$ringlist->[$ring]} ){
		    $NUMRINGSATTHENODE[$node] ++;
		}
		#
		#If perimeter vanishes, i.e. if the polyhedron closes,
		#
		if ( $#newperi == -1 ){
		    #
		    #filter by complexity
		    #
		    my %bonds;
		    my %newlabel;
		    my $nlabel = 0;
		    my $nbond =0;

		    foreach my $ring ( @RINGSINTHEPOLY ){
			my @nodes = @{$ringlist->[$ring]};
			push @nodes, $nodes[0];
			for(my $j=0;$j<$#nodes; $j++){
			    my $x = $nodes[$j];
			    if ( ! defined $newlabel{$x} ){
				$newlabel{$x} = $nlabel ++;
			    }
			    my $y = $nodes[$j+1];
			    if ( ! defined $newlabel{$y} ){
				$newlabel{$y} = $nlabel ++;
			    }
			    #$x = $newlabel{$x};
			    #$y = $newlabel{$y};
			    if ( ! defined $bonds{$x}{$y} ){
				$nbond++;
			    }
			    $bonds{$x}{$y} = 1;
			    $bonds{$y}{$x} = 1;
			}
		    }
		    my $nring = $#RINGSINTHEPOLY + 1;
		    #print STDERR "($nring)";
		    print "$nring - $nbond + $nlabel - 1 \n" if $DEBUG;
		    print "Complexity = ", $nring - $nbond + $nlabel - 1, "\n" if $DEBUG;
		    if ( $nring - $nbond + $nlabel - 1 == 1){
			#
			#Try erasing all the bonds belonging to the fragment
			#from the total network.
			#If resultant graph is disconnected, the fragment
			# contains nodes that are isolated from outer bulk 
			# network. Such a fragment is inappropriate.
			#
			#my $compo = components( \%bonds );
			my $compo = components2( ) - $ORIGINALCOMPO;
			if ( $compo < 0 ){
			  #fragment takes all.
			  $compo = 0;
			}
			if ( $compo == 0 || $NOCHECKCOMPO ){
			    #
			    #check embedded rings which is not counted as a
			    # component of the fragment.
			    #
			    my $multicompo = 0;
			    my @check;
			    foreach my $ring ( @{$ringlist} ){
				my @nodes = @{$ring};
				my $nnodes = $#nodes;
				push @nodes, $nodes[0], $nodes[1];
				for(my $i=0; $i<=$nnodes; $i++ ){
				    my @adjrings = @{$node3->{$nodes[$i+1]}{$nodes[$i]}{$nodes[$i+2]}};
				    foreach my $adj ( @adjrings ){
					if ( ! $PLACED[$adj] ){
					    if ( ! $check[$adj] ){
						my $covered = 1;
						foreach my $node ( @{$ringlist->[$adj]} ){
						    if ( 0 == $NUMRINGSATTHENODE[$node] ){
							$covered = 0;
							last;
						    }
						}
						if ( $covered ){
						    print "ADJ[$adj]" if $DEBUG;
						    $multicompo = 1;
						}
					    }
					    $check[$adj] = 1;
					}
				    }
				}
			    }

			    print join( " ", $#RINGSINTHEPOLY + 1, @RINGSINTHEPOLY ), "\n" if $DEBUG;
			    if ( ! $multicompo ){
				#
				#Output in various formats
				#
				if ( $NGPH ){
				    print "\@RNGS\n$NUMNODES";
				    foreach my $ring ( @RINGSINTHEPOLY ){
					my @nodes = @{$ringlist->[$ring]};
					print join( " ", $#nodes+1, @nodes ), "\n";
				    }
				    print "0\n";
				    print "\@NGPH\n$nlabel\n";
				    foreach my $i ( keys %bonds ){
					foreach my $j ( keys %{$bonds{$i}} ){
					    if ( $i < $j ){
						print "$newlabel{$i} $newlabel{$j}\n";
					    }
					}
				    }
				    print "-1 -1\n";
				}
				if ( $RSET ){
				    print join(" ", $#RINGSINTHEPOLY+1, @RINGSINTHEPOLY ), "\n";
				}
				$NPOLY ++;
			    }
			}
		    }
		}
		else{
		    #
		    # perimeter still exists.
		    #
		    my $error = 0;
		    my $newcenter   = -1;
		    for(my $i=0; $i<=$#newperi; $i++){
			my $node = $newperi[$i];
			if ( 2 < $NUMRINGSATTHENODE[$node] ){
			    $error = 1;
			    last;
			}
			if ( 2 == $NUMRINGSATTHENODE[$node] ){
			    $newcenter = $i;
			}
		    }
		    if ( ! $error ){
			if ( 0 <= $newcenter ){
			    my $newleft = $newcenter - 1;
			    my $newright = $newcenter + 1;
			    if ( $newleft < 0 ){
				$newleft = $#newperi;
			    }
			    if ( $#newperi < $newright ){
				$newright = 0;
			    }
			    ExtendPerimeter( $ringlist, $node3, $originring, \@newperi, $newperi[$newleft], $newperi[$newcenter], $newperi[$newright] );
			}
			else{
			    die "Thin perimeter.\n";
			}
		    }
		}
		#
		#recover perimeter by detaching the ring
		#
		foreach my $node ( @{$ringlist->[$ring]} ){
		    $NUMRINGSATTHENODE[$node] --;
		}
		$PLACED[$ring] = 0;
		pop @RINGSINTHEPOLY;
	    }
	}
    }
}


#
#remove cluster bonds and count num of compos
#
sub components{
    my ( $clusterbonds ) = @_;

    use ogi2;
    my $o = new ogi2( $NUMNODES );

    foreach my $x ( keys %EDGES ){
	foreach my $y ( keys %{$EDGES{$x}} ){
	    if ( $clusterbonds->{$x}{$y} == 0 ){
		$o->add( $x, $y );
	    }
	}
    }
    my $compo = 0;
    for(my $i=0; $i< $NUMNODES; $i++){
	my ( $a, $size ) = $o->query( $i );
	if ( $a == $i ){
	    $compo ++;
	}
    }
    print "Compo $compo\n" if $DEBUG;
    $compo;
}


#
#remove cluster nodes and count num of compos
#
sub components2{
    #
    #ogi2 is the rapid clustering algorithm.
    #
    use ogi2;
    my $o = new ogi2( $NUMNODES );

    foreach my $x ( keys %EDGES ){
	if ( $NUMRINGSATTHENODE[$x] == 0 ){
	    foreach my $y ( keys %{$EDGES{$x}} ){
		if ( $NUMRINGSATTHENODE[$y] == 0 ){
		    $o->add( $x, $y );
		}
	    }
	}
    }
    my $compo = 0;
    for(my $i=0; $i< $NUMNODES; $i++){
	my ( $a, $size ) = $o->query( $i );
	if ( $a == $i && $NUMRINGSATTHENODE[$i] == 0 ){
	    #print "$a $size\n";
	    $compo ++;
	}
    }
    print "Compo $compo\n" if $DEBUG;
    $compo;
}
