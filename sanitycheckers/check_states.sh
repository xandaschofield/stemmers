#!/bin/sh
stempath=~/stemstopped
extension=-out.txt
for corp in arxiv imdb nyt yelp; do
    for stemmer in lemmatized krovetz lovins nostemmer paicehusk porter porter2 sstemmer trunc4 trunc5; do
        for file in $stempath/outs/$corp-$stemmer-*$extension; do
            head -n 4 $file | tail -n 1 >> statestmpfile-$corp-$stemmer.txt
        done
    done
    ntokens=`cat statestmpfile-$corp-*.txt | sort | uniq | wc -l`
    if (( $ntokens == 1 )); then
        echo $corp $t : correct number of tokens
    else
        echo $corp $t : ERROR incorrect number of tokens
        for stemmer in lemmatized krovetz lovins nostemmer paicehusk porter porter2 sstemmer trunc4 trunc5; do
            echo $stemmer
            head -n 1 statestmpfile-$corp-$stemmer.txt
        done
    fi
    rm statestmpfile-$corp-*.txt
done
