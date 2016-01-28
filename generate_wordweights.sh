#!/bin/sh
STEMMER=(lemmatized krovetz lovins nostemmer paicehusk porter porter2 sstemmer trunc4 trunc5)
let "st = $1 % 10"
S=${STEMMER[$st]}
T=$2
K=$3
for file in states/$T-$S-$K-*.gz
do
    bname=`basename $file .gz`
    ~/Mallet/bin/mallet train-topics --input corpora/$T-train-$S.seq --input-state $file --word-topic-counts-file wordweights/$bname.weights --no-inference --num-topics $K
done
