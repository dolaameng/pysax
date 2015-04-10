# pysax
python implementation of SAX (Symbolic Aggregate Approximation) for time series data

## Idea
1. Convert time series data into symbolic representation, where the (Euclidean) distance/similarity is lower bound by the distance in the symbolic space
2. The symbolic representation can be viewed as a low-dim (aggregate) representation of time series
3. Symbol based algorithms such as suffix-tree, markov chain can be used to analyze time-series

## Reference
1. [paper](https://www.google.com.sg/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0CB8QFjAA&url=http%3A%2F%2Fcs.gmu.edu%2F~jessica%2FSAX_DAMI_preprint.pdf&ei=q8AnVezIAc-SuAT14oGwDg&usg=AFQjCNFNhv_-lKglzZvDsuOBirND2ZINeQ&bvm=bv.90491159,d.c2E)
2. [website](http://www.cs.ucr.edu/~eamonn/SAX.htm)
3. [jmotif application](https://code.google.com/p/jmotif/wiki/SAX)
4. [tutorial](http://cs.gmu.edu/~jessica/sax.htm)
5. [R package](http://rug.mnhn.fr/seewave/HTML/MAN/SAX.html)
6. [Another python implementation](https://github.com/nphoff/saxpy)

## Why are we re-implement it?
1. SAX has certain assumptions on time-series data, such as (1) local Gaussian, (2) fixed frequence, (3) real-valued signals. We want to explore more possiblities for other data
2. We want a vector representation of time-series pieces, similiar to the idea of representing words a vectors (Google's word2vec)
3. we need a fast parallel implementation
