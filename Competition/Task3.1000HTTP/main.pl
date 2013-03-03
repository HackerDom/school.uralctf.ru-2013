#!/usr/bin/perl

use FCGI;
use 5.12.00;
use Data::Dumper qw( Dumper );
use threads::shared;
use strict;
# use utf8;
use Encode;
use warnings;
$|++;
use Storable;

binmode STDOUT,':utf8';

my $nameOfCookie_DB:shared='cookies.finilized';
my $nameOfQuestionsDB:shared='DB/questions.finilized';
my $answersRequire=3;

my $DB_questions_dont_forget_fucking_LOCK :shared= retrieve($nameOfQuestionsDB) or die("something wrong with DataBase($nameOfQuestionsDB). $!");
my %h;
my $DB_cookies :shared = \%h;

# say (Data::Dumper::Dumper($DB_questions_dont_forget_fucking_LOCK));

if (-e $nameOfCookie_DB){
	$DB_cookies = retrieve($nameOfCookie_DB);
}else{
    warn("maybe you forget cookie_DB? It must named just as '$nameOfCookie_DB'");
}

sub storeMyCookie{
	lock $DB_cookies;
	store $DB_cookies,$nameOfCookie_DB;
}

sub addCookie{
	my $cookie=shift;
	my $currentScore=shift;
	lock $DB_cookies;
	$DB_cookies->{cookies}->{$cookie}->{score}=$currentScore;
	storeMyCookie;
}

sub returnScore{
	my $cookie=shift;
	lock $DB_cookies;
	return $DB_cookies->{cookies}->{$cookie}->{score};
}

sub isCookieExist{
	my $cookie=shift;
	lock $DB_cookies;
	return (exists $DB_cookies->{cookies}->{$cookie});
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

my $socketToCGI=FCGI::OpenSocket(":9379",5);
print "MAIN";
my $host = FCGI::Request(\*STDIN,\*STDOUT,\*STDERR,\%ENV,$socketToCGI);

my $response;
my $count=1;
my $html;

open FILE,"<","main.html";
read (FILE,$html,1000000);
close FILE;

while($host->Accept()>=0){
	# (threads->create(\&thread_worker,$ENV))->join();
	my %env=%ENV;
	# print "\r\n\r\n";
	my $cookie='';
	$cookie=$env{HTTP_COOKIE} if exists $env{HTTP_COOKIE};
	$cookie=(split"=",$cookie)[1];
	$cookie = '' if !isCookieExist $cookie;
	
	my $isRightAnswer=0;
	
	
	if ($env{REQUEST_METHOD} eq "POST"){
		read (STDIN,$response,$env{HTTP_CONTENT_LENGTH});
		my %post=decodeHEX($response);
		if (exists $post{answer}){
			if ($cookie ne ''){
				if (isRightAnswer($cookie, $post{answer})){
					incScore($cookie);
					$isRightAnswer=1;
				}else{
					DEincScore($cookie);
				}
			}else{
				$cookie=createCookie();
			}
		}
	}else{
		$cookie=createCookie() if ($cookie eq '');
	}
	if (isCompletedTest($cookie)){
		showFlag($cookie);
	}else{
		showPage($cookie,$isRightAnswer);
	}
}

sub thread_worker{
	my %env=@_;
	
	my $cookie='';
	$cookie=$env{HTTP_COOKIE} if exists $env{HTTP_COOKIE};
	$cookie = '' if !isCookieExist $cookie;
	
	my $isRightAnswer=0;
	
	if ($env{REQUEST_METHOD} eq "POST"){
		read (STDIN,$response,$env{HTTP_CONTENT_LENGTH});
		my %post=decodeHEX($response);
		if (exists $post{answer}){
			if ($cookie ne ''){
				if (isRightAnswer($cookie, toInt($post{answer}))){
					incScore($cookie);
					$isRightAnswer=1;
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
	return showPage($cookie,$isRightAnswer);
}

sub isRightAnswer{
	my $cookie=shift;
	my $ans=shift;
	# say "\r\n\r\n '$ans'";
	# say "'".$DB_questions_dont_forget_fucking_LOCK->{returnScore($cookie)}->{rightAnswer}."'";
	return ($DB_questions_dont_forget_fucking_LOCK->{returnScore($cookie)}->{rightAnswer} eq $ans);
}

sub createCookie{
	my $cookie=rand(1000).rand(1000).rand(1000).rand(1000).rand(1000).time;
	addCookie($cookie,1);
	print "Set-Cookie: rrandom=$cookie\r\n";
	# storeMyCookie;
	return $cookie;
}

sub incScore{
	my $cookie=shift;
	addCookie($cookie,returnScore($cookie) + 1);
}	

sub DEincScore{
	my $cookie=shift;
	my $score=returnScore($cookie)-10;
	$score=1 if ($score<1);
	addCookie($cookie,$score);
}	

sub showPage{
	my $cookie=shift;
	my$isRightAnswer=shift;
	
	
	# say "11here11";
	# say $cookie."!";
	
	print "\r\n\r\n";
	
	open HTML,"<:utf8","page.html";
	my $html;
	read HTML,$html,1000000;
	close HTML;
	
	# $html="\r\n\r\n".$html."\r\n\r\n";
	
	my $score=returnScore($cookie);
	
	$html=~s/%question%/normIt($DB_questions_dont_forget_fucking_LOCK->{$score}->{question})/e;
	$html=~s/%currentNumber%/$score/;
	if ($isRightAnswer){
		$html=~s/%status%/correct/;
	}else{
		$html=~s/%status%/uncorrect/;
	}

	my @answers=@{$DB_questions_dont_forget_fucking_LOCK->{$score}->{answers}};

	my $answerBlock='';
	my $index=0;
	
	foreach my $answer(@answers){
		$answerBlock.='<input type="radio" name="answer" value="'.$index++.'">'.normIt($answer).'<br>';
	}
	$html=~s/%answers%/$answerBlock/;

	open FILE,">","log";
	binmode FILE,':utf8';
	say FILE $html;
	close FILE;

	return print $html;
}

sub toInt{
	return ((shift)+0);
}

sub normIt{
return shift;
	return Encode::encode('utf8',shift);
	
	my $body=shift;
	# decode the qouted-printable input
	$body = decode_qp( $body );
	# decode to Perl's internal format
	$body = decode( 'iso-8859-1', $body );
	# encode to UTF-8
	$body = encode( 'utf-8', $body );

	return $body;
}

sub isCompletedTest{
	my $cookie=shift;
	
	my $score = returnScore($cookie);
	
	if ($score>$answersRequire){
		return 1;
	}
	
	return 0;
}

sub showFlag{
	print "\r\n\r\n";
	say "youre welcome\r\n";
	say "access granted\r\n";
	say "your lovely passphraze is\r\n";
	say "whosyourdaddy\r\n";
}
__END__
25. use Storable qw(lock_store lock_nstore lock_retrieve)
26. lock_store \%table, 'file';
27. lock_nstore \%table, 'file';
28. $hashref = lock_retrieve('file');


<input type="radio" name="answer" value="a1">Офицерский состав<Br>
			<input type="radio" name="answer" value="a2">Операционная система<Br>
			<input type="radio" name="answer" value="a3">Большой полосатый му