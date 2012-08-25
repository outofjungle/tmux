#!/usr/bin/env perl

use strict;
use warnings;
use LWP::UserAgent;
use File::Temp;
use Getopt::Long;
use File::Basename qw/basename/;
use JSON qw/from_json to_json/;
use Text::CSV;

my $URI = $ENV{YAHOO_FINANCE_URI} || "http://finance.yahoo.com/d/quotes.csv";
my $TEMP_DIR = "/tmp";
my $DELTA = 600;

my @fields = (
              { id => 's', name => 'symbol' },
              { id => 'l1', name => 'last trade' },
              { id => 'p2', name => 'change percent' },
              { id => 'c1', name => 'change' }
             );

my $opts = { 
            symbol => "YHOO",
            format => "#s:#l1 #c1"
           };

GetOptions (
            "symbol=s" => \$opts->{symbol},
            "format=s" => \$opts->{format}
           ) || usage(1);

my ( $format, $sequence ) = process_user_format( $opts->{format} );
my $quote = get_quote( $opts->{symbol} );

my @output = ( $format );
foreach my $index ( @$sequence ) {
    push @output, $quote->{$fields[$index]->{id}};
}
printf @output;

#
# splits user format into datafield position and format string
#
sub process_user_format {
    
    my $user_f = shift || die "format not found";
    my $print_f = $user_f ."\n";

    my $map = {};
    foreach my $i ( 0 .. $#fields ){
        while ( $user_f =~ m/#(\Q$fields[$i]->{id}\E)/g ) {
            $map->{$-[0]} = $i;
            $print_f =~ s/#(\Q$fields[$i]->{id}\E)/%s/g;
        }
    }
    my @pos = sort { $a > $b } keys %$map;

    my $sequence = [];
    foreach my $i ( @pos ) {
        push @$sequence, $map->{$i};
    }

    return ( $print_f, $sequence );
}

#
# fetches the stock quote
#
sub get_quote {
    
    my $symbol = shift || die "symbol not found";
    my $prefix = basename($0) . "-" . getpwuid( $< ) . "-" . lc( $symbol );
    my @files = <$TEMP_DIR/$prefix-*>; 

    my $cache = {};
    foreach my $file ( @files ) {
        if ( -w $file ) {
            $cache->{file} = $file;
            my @stat = stat( $file );
            $cache->{mtime} = $stat[9];
            last;
        }
    }

    if ( !keys %$cache ) {
        my $tempfile = File::Temp->new( TEMPLATE => "$prefix-XXXXXX",
                                        DIR => $TEMP_DIR,
                                        UNLINK => 0
                                      );
        $cache->{file} = $tempfile->filename;
        $cache->{mtime} = 0;
    }

    my $data = undef;
    if ( time() > $cache->{mtime} + $DELTA ) {

        my $ua = LWP::UserAgent->new;
        $ua->timeout(10);
        $ua->env_proxy;
 
        my $response = $ua->get( $URI . '?f=' . get_id_string(). '&s=' . $opts->{symbol} );
 
        if ($response->is_success) {
            $data = map_fields( $response->decoded_content );
            open my $fh, '>', $cache->{file} or die "can't write to file $cache->{file}: $!\n";
            print $fh to_json( $data );
            close $fh;
        }
    }

    if ( ! $data ) {
        $data = from_json( slurp( $cache->{file} ) );
    }

    return $data;
}

#
# generates query parameter(f) from fields array
#
sub get_id_string {
    my $id_string = '';
    for my $i (0 .. $#fields) {
        $id_string .= $fields[$i]->{id}; 
    }
    return $id_string;
}

#
# maps returned csv fields to a hash using fields array
#
sub map_fields {
    my $content = shift;

    my $csv = Text::CSV->new();
    $csv->parse( $content );
    my @values = $csv->fields();

    my $data = {};
    for my $i (0 .. $#values) {
        $data->{$fields[$i]->{id}} = $values[$i]
    }
    return $data;
}

#
# slurp
#
sub slurp {
    my $file = shift;
    return do {
        local $/ = undef;
        open my $fh, '<', $file or die "can't read contents of $file: $!\n";
        my $content = <$fh>;
        close $fh;
        $content;
    };
}

#
# usage
#
sub usage {
    my $err = shift || 0;
    my $cmd = shift || "";
    $err += 0; # force value to be numeric
    my $io = $err ? \*STDERR : \*STDOUT;
    my $fields = join("\n", map { "        #$_->{id}: $_->{name}" } @fields );

    print $io <<EOM;
Usage:

$0  --symbol <symbol> --format <format>
    - symbol: ticker symbol of the company
    - format: output format string
$fields

EOM

    exit $err;
}
