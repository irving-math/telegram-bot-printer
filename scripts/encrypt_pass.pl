#!/usr/bin/perl -w

$user=$ARGV[0];
$pass=$ARGV[1];

print crypt($user, $pass);
