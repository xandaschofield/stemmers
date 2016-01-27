from collections import Counter


stemmers = ['nostemmer', 'krovetz', 'sstemmer', 'lemmatized', 'porter', 'porter2', 'lovins', 'paicehusk', 'trunc5', 'trunc4']
corpora =  ['arxiv', 'imdb', 'nyt', 'yelp']

def token_length(corp, ty):
    readfiles = [open('corpora/{}-{}-{}-stopped.txt'.format(corp, ty, stemmer)) for stemmer in stemmers]
    character_counts = Counter()
    token_counts = Counter()
    with open('corpora/{}-{}-nostemmer-stopped.txt'.format(corp, ty)) as readref:
        for line in readref:
            stemmedlines = [f.readline() for f in readfiles]
            if not any(stemmedlines):
                continue
            readchunks = [l.split('\t', 2) for l in stemmedlines]
            wordlists = [c[2].split() for c in readchunks]
            for wl, st in zip(wordlists, stemmers):
                character_counts[st] += sum([len(wd) for wd in wl])
                token_counts[st] += len(wl)

    for file in readfiles:
        file.close()

    average_token_lengths = [float(character_counts[st]) / token_counts[st] for st in stemmers]
    return average_token_lengths

if __name__ == '__main__':
    average_tokens_dict = {}
    for corp in corpora:
        average_token_lengths = token_length(corp, 'train')
        average_tokens_dict[corp] = average_token_lengths
    print '\t' + '\t'.join(corpora)
    for i, stemmer in enumerate(stemmers):
        print '{}\t{}'.format(stemmer, '\t'.join(['{:.2f}'.format(average_tokens_dict[corp][i]) for corp in corpora]))

