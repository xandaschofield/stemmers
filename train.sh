#!/bin/sh
STEMMER=(lemmatized krovetz lovins nostemmer paicehusk porter porter2 sstemmer trunc4 trunc5)
let "d = ($1 / 10) % 3"
let "s = $1 % 10"
st=${STEMMER[$s]}
number=$2$1
da=$3
TCOUNTS=(10 50 200)
I=${TCOUNTS[$d]}
~/Mallet/bin/mallet train-topics --input corpora/$da-train-$st.seq --num-topics $I --output-state states/$da-$st-$I-$number.gz --optimize-interval 10 --output-topic-keys keys/$da-$st-$I-$number.keys --num-top-words 20 --diagnostics-file diagnostics/$da-$st-$I-$number.xml --evaluator-filename evaluators/$da-$st-$I-$number.evaluator --topic-word-weights-file wordweights/$da-$st-$I-$number.txt &> outs/$da-$st-$I-$number-out.txt
