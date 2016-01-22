#!/bin/sh
stempath=~/stemstopped
extension=-stopped.txt
for corp in arxiv imdb nyt yelp; do
    for t in test train; do
        for file in ${stempath}/corpora/${corp}-$t-*$extension; do
            wc=`cut -f 3 $file | wc`
            echo $wc $file >> corporatmpfile-$corp-$t.txt
        done
        ntokens=`cat corporatmpfile-$corp-$t.txt | grep -v total | sed 's/  */ /g' | cut -d' ' -f 1-2 | sort | uniq | wc -l`
        nchars=`cat corporatmpfile-$corp-$t.txt | grep -v total | sed 's/  */ /g' | cut -d' ' -f 3 | sort | uniq | wc -l`
        nfiles=`cat corporatmpfile-$corp-$t.txt | grep -v total | wc -l`
        if (( $ntokens == 1 )); then
            echo $corp $t : correct number of tokens
            head -n 1 corporatmpfile-$corp-$t.txt | sed 's/  */ /g' | cut -d' ' -f 1-2
        else
            echo $corp $t : ERROR incorrect number of tokens
            cat corporatmpfile-$corp-$t.txt
        fi
        if (( $nchars == $nfiles )); then
            echo $corp $t : unique stemmers
        else
            echo $corp $t : WARNING stemmers may be identical
            cat corporatmpfile-$corp-$t.txt
        fi
        rm corporatmpfile-$corp-$t.txt
    done
done
