#!/usr/local/bin/perl
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
<img src="../~romance/guestbook/gbtitle.gif" ><BR>
<br>
<p>We use this guestbook as a way of compiling a mailing list so we
can send out<br> tour updates. If you want to contact us, EMAIL US! The
comment section is<br> just that, a comment section. It's not a good way
to contact us or ask questions.<br> Use the sarge e-mail address for
that.</P>
<br>
 <form action="guestbook.cgi" method=post>
<pre>
    Name               <input type=text name=name size=30>
    Email              <input type=text name=email size=30>
    City               <input type=text name=city size=30>
    Country	       <input type=text name=country size=30>
    URL  (optional)    <input type=text name=url value="http://" size=30>


    Comments  	       <textarea name=suggestions rows=4 cols=30></textarea><p>

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

$name = &grab($input, "name");
$email = &grab($input, "email");
$city = &grab($input, "city");
$url = &grab($input, "url");
$country = &grab($input, "country");
$suggestions = &grab($input, "suggestions");


$date = `/bin/date '+%A %r %D'`;
chop $date;


open(MAIL, "| /usr/bin/sendmail -t") || die "Cannot sendmail: $!\n";
print MAIL "From: GuestBook\@shout.net\n";
print MAIL "To: sarge\@prairienet.org\n";
print MAIL "Subject: New addition to the Sarge Guestbook\n";
print MAIL "\n";
print MAIL "Date: $date\n";
print MAIL "Email: $email\n";
print MAIL "Name: $name\n";
print MAIL "City: $city\n";
print MAIL "URL: $url\n";
print MAIL "Comments:\n";
print MAIL "$suggestions\n";

close(MAIL);

open (GUESTBOOK, "/home/users/sub/romance/public_html/guestbook/guestlog.html") || die "Cannot open guestlog\n";
open (NEWGUESTBOOK, ">/home/users/sub/romance/public_html/guestbook/guestlog.new.html") || die "Cannot open new guestlog\n";
while (<GUESTBOOK>) {
	if (/NEWLOG>/) {
		print NEWGUESTBOOK <<EOF;
<NEWLOG>
<CENTER><P>
<TABLE WIDTH=468 BORDER=0 CELLSPACING=0 CELLPADDING=1>
<TR><TD>
<B>Name:</B> <A HREF="mailto:$email" COLOR="#CC000">$name</A><BR>
City: $city <BR>
Country: $country<BR>
EOF

	       #if ( $url !eq "http://" ) 
	       	    print NEWGUESTBOOK "URL: <A HREF=\"$url\">$url</A><BR>\n" if ($url ne "http://");
	       print NEWGUESTBOOK <<EOF;
Comments: <B><BLOCK>$suggestions</BLOCK></B><BR>
<DIV align=right><SMALL>$date</SMALL></DIV><BR></TD></TR></TABLE>
<HR size=1 WIDTH=468>
</CENTER>
EOF

		}
	else 	
	{
		print NEWGUESTBOOK "$_";	
	}
	
}
close(GUESTBOOK);
close(NEWGUESTBOOK);
$hack = `cp /home/users/sub/romance/public_html/guestbook/guestlog.new.html /home/users/sub/romance/public_html/guestbook/guestlog.html`;

print "Content-type: text/html\n\n";
open (DONEGUESTBOOK, "/home/users/sub/romance/public_html/guestbook/guestlog.html");
while (<DONEGUESTBOOK>) {
	print $_;
}
close (DONEGUESTBOOK);
