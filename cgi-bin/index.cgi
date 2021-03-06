#!/usr/bin/perl
use CGI qw/:standard/;
use strict;
use warnings;
use DBI;
use utf8;
use CGI::Carp qw(fatalsToBrowser);
binmode(STDOUT,':utf8');

my $cgi = new CGI;

require "../config.pl";

our %conf;

my $dbh = DBI->connect(
    "DBI:mysql:" . $conf{dbuser} . ":" . $conf{dbhost}, 
    $conf{dbuser}, 
    $conf{dbpasswd}, 
    {
        mysql_enable_utf8 => 1
    }
);

$dbh->do("set names utf8");

my $sth = $dbh->prepare("SELECT INET_NTOA(ip), name FROM olt;");
$sth->execute;

print $cgi->header(
    -charset=>'UTF-8'
);

print $cgi->start_html(
    -title=>'Cdata Control',
    -style=>{'src'=>'/cdata/style.css'}
);

print qq'<div class="block-round-content">Панель управления Cdata</div>';

if ($ENV{'HTTP_ACCEPT'}){
    &index;
}

sub index {
    print qq'<table border=1><tr><th>IP</th><th>Имя</th></tr>';
    while (my $ref = $sth->fetchrow_hashref()) {
        print "<tr onclick=\"document.location = 'olt.cgi?$ref->{'INET_NTOA(ip)'}'\" >";
        print "<td>", $ref->{'INET_NTOA(ip)'},"</td>";
        print "<td>", $ref->{'name'},"</td>";
    }
    print qq'</table>';
}
print qq'<p><a href="add.cgi">Добавить</a></p>';

$sth->finish;
$dbh->disconnect;
