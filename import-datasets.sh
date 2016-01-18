#!/bin/sh
# DATA=(arxiv imdb nyt yelp)
STEMMER=(lemmatized krovetz lovins nostemmer paicehusk porter porter2 sstemmer trunc4 trunc5)
# let "d=$1/10"
let "s=$1%10"
st=${STEMMER[$s]}
for da in arxiv imdb nyt yelp
do
    ~/Mallet/bin/mallet import-file --input corpora/$da-train-${st}-stopped.txt --output corpora/$da-train-$st.seq --keep-sequence --token-regex "[\p{L}]+"
    ~/Mallet/bin/mallet import-file --input corpora/$da-test-${st}-stopped.txt --output corpora/$da-test-$st.seq --keep-sequence --token-regex "[\p{L}]+" --use-pipe-from corpora/$da-train-$st.seq
done
