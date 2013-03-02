use Storable;
use 5.12.00;
use Encode;
use utf8;
use Data::Dumper qw( Dumper );
use XML::Simple qw(:strict);

my @xml_files=qw/1 2 3 4 5 6 7 8 9/;

foreach my $xml_file(@xml_files){

	open XML,"<:utf8",'prepared tests/'.$xml_file or die $!;

	my $file;
	read XML, $file,1000000000;

	$file=~s/Заголовок/head/g;
	$file=~s/Вопрос/question/g;
	$file=~s/Ид=/ID=/g;
	$file=~s/ВариантОтвета/answerPoint/g;
	$file=~s/Анкета/form/g;
	$file=~s/Группа/group/g;
	$file=~s/Наименование/value/g;


	my $config = XMLin($file, KeyAttr => { "group" => 'ID' }, ForceArray => ["group","answerPoint"]);

	# say $file;

	# say Encode::encode('UTF-8',((${$config->{form}->{group}->{'487fbc80-111b-11e2-a4a4-001d09b78380'}->{question}}[0])->{answerPoint}[0])->{value });

	open FILE,">:utf8","refactored tests/".$xml_file.".factored";

	binmode(FILE);

	say FILE  $file;


	close FILE;

	open FILE,">:utf8","refactored tests/".$xml_file.".dumped";

	binmode(FILE);

	my $text=Data::Dumper::Dumper($config);

	$text=Encode::encode('UTF-8',($text));


	say FILE  $text;


	close FILE;
}
__END__
`


open FILE,">:utf8","ans.txt";

binmode(FILE);

say FILE Data::Dumper::Dumper($config);


close FILE;
# store \%table, 'file';

# my $hashref = retrieve('file');

# say ;
