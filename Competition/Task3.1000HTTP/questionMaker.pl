#!/usr/bin/perl

use Storable;
use 5.12.00;
use Encode;
use utf8;
use Data::Dumper qw( Dumper );
use XML::Simple qw(:strict);

my @xml_files=qw/1 2 3 4 5 6 7 8 9/;

my @questions;

foreach my $xml_file(@xml_files){
	 

	open XML,"<:utf8","refactored tests/".$xml_file.".factored";

	my $file;
	read XML, $file,1000000000;

	my $config = XMLin($file, KeyAttr => { "group" => 'ID' }, ForceArray => ["group","answerPoint"]);
	
	# say Data::Dumper::Dumper($config);
	
	push @questions,returnQuestions_1($config);
	# say Data::Dumper::Dumper(\@questions);
	# say Encode::encode('cp866',Data::Dumper::Dumper(\@ar));
	# say $file;
	
	#say Encode::encode('cp866',((${$config->{form}->{group}->{'487fbc80-111b-11e2-a4a4-001d09b78380'}->{question}}[0])->{answerPoint}[0])->{value });
}

toUsable_2(@questions);

sub returnQuestions_1{
	my $main=shift;
	
	my @questions;
	# say Data::Dumper::Dumper($main);
	foreach my $groups(keys %{$main->{form}->{group}}){
		foreach my $question($main->{form}->{group}->{$groups}->{question}){
			push @questions, $question;
		}
	}
	
	return $questions[0];
}

sub toUsable_2{
	my @questions = @_;
	
	my %memory;
	my $id=0;
	
	# say Data::Dumper::Dumper(\%memory);
	
	foreach my $block_test(@questions){
		foreach my $block_question(@$block_test){
			# say $block_question;
			$memory{++$id}->{question}=$block_question->{value};
			$memory{$id}->{answers}=[];
			my $countOfpoints=0;
			foreach my $answer ( @{$block_question->{answerPoint}}){
				if ($answer->{value} ne ''){
					push @{$memory{$id}->{answers}},$answer->{value};
					++$countOfpoints;
				}
			}
			$memory{$id}->{rightAnswer}= int(rand($countOfpoints));
		}
	}
	
	say $id;
	store \%memory,'questions.finilized';

    my $test=retrieve('questions.finilized');

    print Data::Dumper::Dumper($test);
	
	my %memory;
	my $id=0;
	
	# say Data::Dumper::Dumper(\%memory);
	
	foreach my $block_test(@questions){
		foreach my $block_question(@$block_test){
			# say $block_question;
			$memory{++$id}->{question}=normIt($block_question->{value});
			$memory{$id}->{answers}=[];
			my $countOfpoints=0;
			foreach my $answer ( @{$block_question->{answerPoint}}){
				if ($answer->{value} ne ''){
					push @{$memory{$id}->{answers}},normIt($answer->{value});
					++$countOfpoints;
				}
			}
			$memory{$id}->{rightAnswer}= int(rand($countOfpoints));
		}
	}
	
	#say Data::Dumper::Dumper(\%memory);
}

sub normIt{
	return Encode::encode('utf8',shift);
}
