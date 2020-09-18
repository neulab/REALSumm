#!/bin/bash
# rename files in <dir> (in-place) by adding an integer to the document id
# file name format should be like out_doc_<int>_bertscore_53.42
# usage: ./rename_files <dir> <integer>
#echo $1
#echo $2
for f in $1/* ; do n=$(echo $f | cut -d '_' -f 3) ; m=`expr $n + $2`; new_f="$(echo $f | sed "s/$n/$m/g")" ; mv $f $new_f ; done

