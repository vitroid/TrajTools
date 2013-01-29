package main;

BEGIN{
    push(@INC,"/u/matto/src/Tools/Traj2Mol3")
}

use strict;

sub new{
    my ( $package, $self ) = @_;
    bless $self, $package;
}


sub loop{
    my ( $self ) = @_;

    while(<STDIN>){
	if(/\@BOX3/){
	    $_=<STDIN>;
	    chomp;
	    $self->{box} = new Box( split );
	    $self->{output}->SetBox( $self->{box} );
	}elsif(/\@BXLA/){
	    my $x = <STDIN>;
	    $self->{box} = new Box( $x, $x, $x );
	    $self->{output}->SetBox( $self->{box} );
	}elsif(/\@ID08/){
	    $self->{id08} = <STDIN>;
	}elsif(/\@NGPH/||/\@BMRK/){
	    $self->{bondlayer}->load;
	    $self->{bondcolor}->load;
	    $self->{ngph}++;
	    $self->{bmrk}++ if(/\@BMRK/);
	    my $n=<STDIN>;
	    $self->{nhb}=0;
	    $self->{hb}=[];
	    $self->{hb1}=[];
	    $self->{hb2}=[];
	    $self->{hb3}=[];
	    while(<STDIN>){
		my ($x,$y,$z)=split;
		last if($x<0);
		$self->{hb1}[$self->{nhb}]=$x;
		$self->{hb2}[$self->{nhb}]=$y;
		$self->{hb3}[$self->{nhb}]=$z;
		$self->{nhb}++;
		$self->{hb}[$x]++;
		$self->{hb}[$y]++;
	    }
	}elsif(/^\@NX3A/||/^\@NX4A/||/^\@AR3A/||/^\@WTG3/){
	    chomp;
	    my $id=$_;
	    #unless ($firstpage){
	    #    $output->newpage();
	    #}
	    #$firstpage = 0;
	    $self->{nodelayer}->load;
	    $self->{nodecolor}->load;
	    $self->{nx3a}++;
	    print STDERR "[$self->{nf}]";
	    $self->{nf}++;
	    my $n=<STDIN>;
	    my ($h1,$h2,$o);
	    $h1=$h2=$o="";
	    #my @oldmol=@{$self->{mol}};
	    $self->{mol} = [];
	    $self->{output}->startpage();
	    for(my $i=0;$i<$n;$i++){
		$_=<STDIN>;
		chomp;
		@_=split;
		if ( $self->{id08} =~ /^TIP4P   / ){
		    require "RigidWater.pm";
		    $self->{mol}[$i] = RigidWater->new( output=>$self->{output},
					       shownum=>$self->{num},
					       box=>$self->{box},
					       order=>$i );
		}
		elsif ( $self->{id08} =~ /^SJBENZEN/ ){
		    require "RigidBenzene.pm";
		    $self->{mol}[$i] = new RigidBenzene( output=>$self->{output},
						 shownum=>$self->{num},
						 box=>$self->{box},
						 order=>$i );
		}
		else {
		    if($id =~ /\@NX[34]A/ || $id =~ /\@WTG3/){
			require "RigidWater.pm" || die;
			#print STDERR join(":", @INC );
			$self->{mol}[$i] = RigidWater->new( output=>$self->{output},
						   shownum=>$self->{num},
						   box=>$self->{box},
						   order=>$i );
		    }
		    else{
			require "Atomic.pm";
			$self->{mol}[$i] = Atomic->new( output=>$self->{output},
					       shownum=>$self->{num},
					       box=>$self->{box},
					       order=>$i );
		    }
		}
		$_[0]+=$self->{offsetx};
		$_[1]+=$self->{offsety};
		$_[2]+=$self->{offsetz};
		$self->{mol}[$i]->config( @_ );
		
		$self->{output}->SetLayer( $self->{nodelayer}->value( $i ) );
		$self->{output}->SetPalette( $self->{nodecolor}->value( $i ) );
		$self->{mol}[$i]->draw();
	    }
	}
	if($self->{ngph}&&$self->{nx3a}){
	    #
	    #付帯情報を読みこむ
	    #
	    $self->{ngph}=$self->{nx3a}=0;
	    for(my $k=0;$k<$self->{nhb};$k++){
		my $i = $self->{hb1}[$k];
		my $j = $self->{hb2}[$k];
		$self->{output}->SetLayer( $self->{bondlayer}->value( $i, $j ) );
		$self->{output}->SetPalette( $self->{bondcolor}->value( $i, $j ) );
		$self->{mol}[$i]->drawbond( $self->{mol}[$j] );
	    }
	    if ( $self->{postprocess} ){
		foreach my $postprocess ( @{$self->{postprocess}} ){
		    $postprocess->execute( $self );
		}
	    }
	    $self->{output}->newpage();
	}
    }
}


    
1;
