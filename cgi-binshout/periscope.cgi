#!/bin/sh

#
# Script to gather results from the surrealist survey and mail them
# the to server adminstrator.  This version actually mails the results.

TMP=/tmp/mailcensus.$$

echo "Surrealist Census Results" >> $TMP
echo "----------------------" >> $TMP
echo >> $TMP
echo "Name: $WWW_theName" >> $TMP
echo "Sex:  $WWW_theSex" >> $TMP
echo >> $TMP
echo "Contains:" >> $TMP

if [ "$WWW_humor" = "on" ]; then
        echo "   Vitreous Humor" >> $TMP
fi

if [ "$WWW_fish" = "on" ]; then
        echo "   Fish" >> $TMP
fi

if [ "$WWW_glycol" = "on" ]; then
        echo "   Propylene Glycol" >> $TMP
fi

if [ "$WWW_svga" = "on" ]; then
        echo "   SVGA Support" >> $TMP
fi

if [ "$WWW_angst" = "on" ]; then
        echo "   Angst" >> $TMP
fi

if [ "$WWW_catcon" = "on" ]; then
        echo "   Catalytic Converter" >> $TMP
fi

if [ "$WWW_vitamin" = "on" ]; then
        echo "   Ten Essential Vitamins and Minerals" >> $TMP
fi

# You've got all the results formatted in the temp file, now
# mail and remove it.
mail -s "Survey Results" romance@shout.net < $TMP
rm $TMP

# Finally, give a nice message back to your reader.
#
echo Content-type: text/html
echo

echo   "<HTML><HEAD>"
echo   "<TITLE>The Surrealist Census:  Thank You</TITLE>"
echo   "</HEAD><BODY>"
echo   "<H1>Thank you for voting!</H1>"
echo   "<P>Your votes in the Surrealist Census will be tallied and "
echo   "used for reasons wholly inappropriate to herding sheep."
echo   "</BODY></HTML>"


