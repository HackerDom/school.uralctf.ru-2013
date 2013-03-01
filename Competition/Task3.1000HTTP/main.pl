#!/usr/bin/perl

use FCGI;
use 5.12.00;
use Data::Dumper qw( Dumper );
use threads::shared;
use strict;
use warnings;

use Storable;

my $nameOfCookie_DB:shared='cookies.finilized';
my $nameOfQuestionsDB:shared='q_formed_DB.finilized';

my $DB_questions_dont_forget_fucking_LOCK :shared= retrieve($nameOfQuestionsDB) or die("something wrong with DataBase($nameOfQuestionsDB). $!");
my $DB_cookies :shared = \(my %h);

say (Data::Dumper::Dumper($DB_questions_dont_forget_fucking_LOCK));

if (-e $nameOfCookie_DB){
	$DB_cookies = retrieve($nameOfCookie_DB);
}else{
    warn("maybe you forget cookie_DB? It must named just as '$nameOfCookie_DB'");
}

sub storeMyCookie{
	lock $nameOfCookie_DB;
	store $nameOfCookie_DB,$nameOfCookie_DB;
}

sub addCookie{
	my $cookie=shift;
	my $currentScore=shift;
	lock $nameOfCookie_DB;
	$nameOfCookie_DB->{cookies}->{$cookie}->{score}=$currentScore;
}

sub returnScore{
	my $cookie=shift;
	lock $nameOfCookie_DB;
	return $nameOfCookie_DB->{cookies}->{$cookie}->{score};
}

sub isCookieExist{
	my $cookie=shift;
	lock $nameOfCookie_DB;
	return exists $nameOfCookie_DB->{cookies}->{$cookie};
}

sub getQuestion{
	my $number=shift;
	return $DB_questions_dont_forget_fucking_LOCK->{$number}
}


sub decodeHEX{
	my $query=shift;
	$query =~ s/\+/ /g;
	$query  =~ s/%([0-9A-H]{2})/pack('C', hex($1))/eg;
	my %ans;
	%ans=map {split('=',$_)} (split('&',$query));
	#print %ans;
	return %ans;
	#return split('=',(split('&',$query)));
}

my $socketToCGI=FCGI::OpenSocket(":1337",5);
print "MAIN";
my $host = FCGI::Request(\*STDIN,\*STDOUT,\*STDERR,\%ENV,$socketToCGI);

my $response;
my $count=1;
my $html;

open FILE,"<","main.html";
read (FILE,$html,1000000);
close FILE;

while($host->Accept()>=0){
	(threads->create(\&thread_worker,$ENV))->join();
}

sub thread_worker{
	my %env=@_;
	
	my $cookie='';
	$cookie=$ENV{HTTP_COOKIE} if exists $ENV{HTTP_COOKIE};
	$cookie = '' if !isCookieExist $cookie;
	if ($ENV{REQUEST_METHOD} eq "POST"){
		read (STDIN,$response,$env{HTTP_CONTENT_LENGTH});
		my %post=decodeHEX($response);
		if (exists $post{answer}){
			if ($cookie ne ''){
				if (isRightAnswer($cookie, toInt($post{answer}))){
					incScore($cookie);
				}else{
					DEincScore($cookie);
				}
			}else{
				createCookie();
			}
		}
	}else{
		createCookie() if ($cookie eq '');
	}
	return showPage($cookie);
}

sub isRightAnswer{
	my $cookie=shift;
	my $ans=shift;
	
	return ($h{asks}->{returnScore($cookie)}->{rightAnswer} eq $ans);
}

sub createCookie{
	my $cookie=rand(1000).rand(1000).rand(1000).rand(1000).rand(1000);
	addCookie($cookie,1);
	print "Set-Cookie: $cookie\r\n";
	return storeMyCookie;
}

sub incScore{
	my $cookie=shift;
	addCookie($cookie,returnScore($cookie) + 1);
}	

sub DEincScore{
	my $cookie=shift;
	addCookie($cookie,returnScore($cookie) - 10);
}	

sub showPage{
	my $cookie=shift;
	
	print "\r\n\r\n";
	#content....
	return
}
