#!/usr/bin/perl
#
# sarge guestbook Version 0.991

# Copyright (c) 1998  Erik Wolf
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice in the documentation and/or other materials provided with
#    the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# IF YOU DON"T LIKE THIS LICENSE, THEN FUCK OFF!!!!!!!!!!!

sub grab {
  local($inp, $tinp, $name, $part, $tpart, $ind);
  $inp = "&" . $_[0] . "&";
  $name = $_[1];
  $tinp = $inp;
  $part = "";

  for (;;) {
    ($tpart) = ($tinp =~ /&$name=([^&]*)&/);
    $ind = index($tinp, "$name=$tpart") + length("$name=$tpart");
    $tpart =~ tr/+/ /;
    $tpart =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $tpart =~ s/\r//eg;
    if ($tpart eq "") {
      last;
    }

    if ($part ne "") {
      $part = "$part, $tpart";
    } else {
      $part = $tpart;
    }

    $tinp = substr($tinp, $ind);
    if ($tinp eq "") {
      last;
    }
  }

  $part;
}

sub print_form {
print "Content-type: text/html\n\n";
print <<EOF;

<html>
<head>
<title>Sarge Guestbook</title>
</head>

<body bgcolor=#ffffff>
<img src="http://www.shout.net/~romance/guestbook/gbtitle.gif" ><BR>
<form action="guestbook.cgi" method=post>
<pre>
    Email              <input type=text name=email size=30>
    
		       <input type=submit value=Submit!>
</pre>
</form>
</body>
</html>
EOF
}

$content_length = $ENV{"CONTENT_LENGTH"};
read(STDIN, $input, $content_length);

if ($content_length == 0) {
  &print_form;
  exit 0;
} 

$email = &grab($input, "email");


$date = `/bin/date '+%A %r %D'`;
chop $date;


open(MAIL, "| /usr/bin/sendmail -t") || die "Cannot sendmail: $!\n";
print MAIL "From: Maillist\@shout.net\n";
print MAIL "To: romance\@shout.net\n";
print MAIL "Subject: New addition to the Mail list\n";
print MAIL "\n";
print MAIL "Date: $date\n";
print MAIL "Email: $email\n";

close(MAIL);

