#!/bin/sh
arr=(krovetz lovins nostemmer paicehusk porter porter2 sstemmer trunc4 trunc5 lemmatized)
N=$1
T=$2
let "i = $3 % 10"
for file in modstates/$N-${arr[$i]}-$T-*.gz
do
    bname=`basename $file .gz`
    ~/Mallet/bin/mallet train-topics --input corpora/$N-train-nostemmer.seq --input-state $file --num-topics $T --no-inference --diagnostics-file coherences/$bname.xml --num-top-words 15 &> coherenceouts/$bname.out
done
