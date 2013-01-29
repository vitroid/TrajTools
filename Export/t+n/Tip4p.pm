# -*- perl -*-
package Tip4p;
use strict;
BEGIN{
    use Exporter ();
    use vars qw(@ISA @EXPORT @EXPORT_OK);
    @ISA       = qw(Exporter);
    @EXPORT    = qw(tip4pnx4a tip4pconf);
    @EXPORT_OK = qw();
}

use vars @EXPORT_OK;

my $angle=104.5*3.14159/360;
my $holen=0.9572;
my $ohz=$holen*cos($angle);
my $hyl=$holen*sin($angle);
my $hzl=16*$ohz/18;
my $ol=-$ohz+$hzl;

sub tip4pconf{
    my($a,$b,$c)=@_;
    my $sina=sin($a);
    my $sinb=sin($b);
    my $sinc=sin($c);
    my $cosa=cos($a);
    my $cosb=cos($b);
    my $cosc=cos($c);
    my $sp12=-($sinc*$cosb+$cosa*$sinb*$cosc);
    my $sp13=$sina*$sinb;
    my $sp22=-$sinc*$sinb+$cosa*$cosb*$cosc;
    my $sp23=-$sina*$cosb;
    my $sp32=$sina*$cosc;
    my $sp33=$cosa;
    my $sy12=$sp12*$hyl;
    my $sy22=$sp22*$hyl;
    my $sy32=$sp32*$hyl;
    my $sz13=$sp13*$hzl;
    my $sz23=$sp23*$hzl;
    my $sz33=$sp33*$hzl;
    my $xx0=$sy12+$sz13;
    my $yy0=$sy22+$sz23;
    my $zz0=$sy32+$sz33;
    my $xx1=-$sy12+$sz13;
    my $yy1=-$sy22+$sz23;
    my $zz1=-$sy32+$sz33;
    my $xx2=$sp13*$ol;
    my $yy2=$sp23*$ol;
    my $zz2=$sp33*$ol;
    ($xx2,$yy2,$zz2,$xx0,$yy0,$zz0,$xx1,$yy1,$zz1);
}

sub tip4pnx4a{
    my($a,$b,$c,$d)=@_;
    my $sp11=($a*$a+$b*$b-($c*$c+$d*$d));
    my $sp12=-2.0*($a*$d+$b*$c);
    my $sp13=2.0*($b*$d-$a*$c);
    my $sp21=2.0*($a*$d-$b*$c);
    my $sp22=$a*$a+$c*$c-($b*$b+$d*$d);
    my $sp23=-2.0*($a*$b+$c*$d);
    my $sp31=2.0*($a*$c+$b*$d);
    my $sp32=2.0*($a*$b-$c*$d);
    my $sp33=$a*$a+$d*$d-($b*$b+$c*$c);
    my $sy12=$sp12*$hyl;
    my $sy22=$sp22*$hyl;
    my $sy32=$sp32*$hyl;
    my $sz13=$sp13*$hzl;
    my $sz23=$sp23*$hzl;
    my $sz33=$sp33*$hzl;
    my $xx0=$sy12+$sz13;
    my $yy0=$sy22+$sz23;
    my $zz0=$sy32+$sz33;
    my $xx1=-$sy12+$sz13;
    my $yy1=-$sy22+$sz23;
    my $zz1=-$sy32+$sz33;
    my $xx2=$sp13*$ol;
    my $yy2=$sp23*$ol;
    my $zz2=$sp33*$ol;
    ($xx2,$yy2,$zz2,$xx0,$yy0,$zz0,$xx1,$yy1,$zz1);
}

1;
