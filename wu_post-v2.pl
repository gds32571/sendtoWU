#!/usr/bin/perl

# gswann 7 November 2015
# see http://wiki.wunderground.com/index.php/PWS_-_Upload_Protocol
# No! See: https://feedback.weather.com/customer/en/portal/articles/2924682-pws-upload-protocol?b_id=17298
# for description of protocol

open(my $fh, "secrets.txt")
    or die "Could not open file";

    my $row = <$fh>;
    chomp $row;
    $ID = $row;
    my $row = <$fh>;
    chomp $row;
    $PW = $row;
    close $fh;

$str1 = "http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID=";
$str2 = "&PASSWORD=";
$str3 = "&dateutc=now";
$str35 = "&tempf=";
$str36 = "&temp2f=";
$str4 = "&humidity=";
$str45 = "&dewptf=";

$str6 = "&windspeedmph=";
$str7 = "&winddir=";

$str9 = "&action=updateraw";

$degrees = <stdin>;
$humidity = <stdin>;
$windspeed = <stdin>;
$winddir = <stdin>;
$degrees2 = <stdin>;

if ($degrees != "un"){
    $celsius = (($degrees-32.0)*5.0)/9.0 ;
    $dewpoint = $celsius - ((100-$humidity) / 5.00) ;
    $dewpoint = (($dewpoint * 9.0 ) / 5.0) + 32.0;
}

print ("Degrees= $s  ", $degrees);
print ("  Humidity = $s  ", $humidity) ;
printf ("  Dew point = %3.3f  ", $dewpoint) ;
printf ("  Windspeed = $s ", $windspeed);
printf ("  Winddir = $s ", $winddir);
printf ("  Lanai temp = $s ", $degrees2);
print ("\n");

if ($degrees != "un"){
    $degrees = sprintf("%.1f",$degrees);
}

printf($degrees);
print ("\n");

if ($degrees2 != "un"){
    $degrees2 = sprintf("%.1f",$degrees2);
}

printf($degrees2);
print ("\n");


if ($humidity != "un"){
    $humidity = sprintf("%.0f",$humidity);
}

if ($windspeed != "un"){
    $windspeed = sprintf("%.1f", $windspeed);
}

if ($winddir != "un"){
    $winddir = sprintf("%.0f", $winddir);
}

printf($humidity);
print ("\n");
printf($windspeed);
print ("\n");
printf($winddir);
print ("\n");
$dewpoint = sprintf("%.0f",$dewpoint);
printf($dewpoint);
print ("\n");

# $getstr = $str1 . $ID . $str2 . $PW . $str3 . $degrees . $str4 . $humidity . $str45 . $dewpoint . $str6 . $windspeed . $str7 . $winddir . $str9   ;

$getstr = $str1 . $ID . $str2 . $PW . $str3 ;

if ($degrees != "un" ) { $getstr = $getstr . $str35 . $degrees ;}
if ($humidity != "un" ) { $getstr = $getstr . $str4 . $humidity ;}
if ($dewpoint != "un") {  $getstr = $getstr . $str45 . $dewpoint;}
if ($windspeed != "un" ) { $getstr = $getstr . $str6 . $windspeed ;}
if ($winddir != "un" ) { $getstr = $getstr . $str7 . $winddir ;}
if ($degrees2 != "un") { $getstr = $getstr . $str36 . $degrees2 ;}
$getstr = $getstr . $str9  ;

print $getstr;
print ("\n"); 

system ("wget \"" . $getstr . "\" -O result.txt");

