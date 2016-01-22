#!/bin/sh

for corp in arxiv imdb nyt yelp; do
    for top in 10 50 200; do
        cat vois/voi-$corp-$top-*-*.voi | grep -v '#' | grep -v Java > vois/$corp-$top.voi
    done
done
