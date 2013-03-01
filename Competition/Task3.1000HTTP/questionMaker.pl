#!/usr/bin/perl

use Storable;
use 5.12.00;
use Encode;
use utf8;


my %h;
$h{asks}->{1}->{question}='who is your daddy?';
$h{asks}->{1}->{points}=['he is my daddy','you is my daddy','nobody.one'];
$h{asks}->{1}->{rightAnswer}=$h{asks}->{1}->{points}[2];

store \%h,"fresh";