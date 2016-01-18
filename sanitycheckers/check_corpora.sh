#!/bin/sh
extension=-stopped.txt
for corp in arxiv imdb nyt yelp; do
    for t in test train; do
        wc ../corpora/$corp-$t-*$extension > corporatmpfile-$corp-$t.txt
        ntokens=`cat corporatmpfile-$corp-$t.txt | grep -v total | sed 's/  */ /g' | cut -d' ' -f 2-3 | sort | uniq | wc -l`
        nchars=`cat corporatmpfile-$corp-$t.txt | grep -v total | sed 's/  */ /g' | cut -d' ' -f 4 | sort | uniq | wc -l`
        nfiles=`cat corporatmpfile-$corp-$t.txt | grep -v total | wc -l`
        if (( $ntokens == 1 )); then
            echo $corp $t : correct number of tokens
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
