#!/bin/sh
STEMMER=(lemmatized krovetz lovins nostemmer paicehusk porter porter2 sstemmer trunc4 trunc5)
let "st = $1 % 10"
S=${STEMMER[$st]}
T=$2
for file in evaluators/$T-$S-*-*.evaluator
do
    bname=`basename $file .evaluator`
    if [ ! -f outprobs/$bname.outprob ]; then
        ~/Mallet/bin/mallet evaluate-topics --show-words --input corpora/$T-test-$S.seq --evaluator $file --output-prob outprobs/$bname.outprob --output-doc-probs docprobs/$bname.docprobs > wordprobs/$bname.wordprobs
    fi
done
