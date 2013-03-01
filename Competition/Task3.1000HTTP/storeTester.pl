use Storable;
use 5.12.00;
use Encode;
use utf8;
use Data::Dumper qw( Dumper );
use XML::Simple qw(:strict);

my $xml_file="third.xml";

open XML,"<:utf8",$xml_file;

my $file;
read XML, $file,1000000000;

$file=~s/Заголовок/head/g;
$file=~s/Вопрос/Answer/g;
$file=~s/Ид=/ID=/g;
$file=~s/ВариантОтвета/answerPoint/g;
$file=~s/Анкета/form/g;
$file=~s/Группа/group/g;
$file=~s/Наименование/value/g;


# my $config = XMLin($file, KeyAttr => { "Группа" => 'ИД' }, ForceArray => ["Группа","ВариантОтвета"]);

# say $file;


open FILE,">:utf8","ans.txt";

binmode(FILE);

say FILE  $file;


close FILE;

__END__



open FILE,">:utf8","ans.txt";

binmode(FILE);

say FILE Data::Dumper::Dumper($config);


close FILE;
# store \%table, 'file';

# my $hashref = retrieve('file');

# say ;
