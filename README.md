# pysax
python implementation of SAX (Symbolic Aggregate Approximation) for time series data

## Idea
1. Convert time series data into symbolic representation, where the (Euclidean) distance/similarity is lower bound by the distance in the symbolic space
2. The symbolic representation can be viewed as a low-dim (aggregate) representation of time series
3. Symbol based algorithms such as suffix-tree, markov chain can be used to analyze time-series

## References
1. [paper](https://www.google.com.sg/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0CB8QFjAA&url=http%3A%2F%2Fcs.gmu.edu%2F~jessica%2FSAX_DAMI_preprint.pdf&ei=q8AnVezIAc-SuAT14oGwDg&usg=AFQjCNFNhv_-lKglzZvDsuOBirND2ZINeQ&bvm=bv.90491159,d.c2E)
2. [website](http://www.cs.ucr.edu/~eamonn/SAX.htm)
3. [jmotif application](https://code.google.com/p/jmotif/wiki/SAX)
4. [tutorial](http://cs.gmu.edu/~jessica/sax.htm)
5. [R package](http://rug.mnhn.fr/seewave/HTML/MAN/SAX.html)
6. [Another python implementation](https://github.com/nphoff/saxpy)
7. [GrammarVis](http://grammarviz2.github.io/grammarviz2_site/)
8. [GrammarVis github](https://github.com/GrammarViz2/grammarviz2_src)
9. [GrammarVis VSM github](https://github.com/jMotif/sax-vsm_classic)
10. [jMotif github](https://github.com/jMotif/SAX)

## Why are we re-implementing it?
1. SAX has certain assumptions on time-series data, such as (1) local Gaussian, (2) fixed frequence, (3) real-valued signals. We want to explore more possiblities for other data
2. We want a vector representation of time-series pieces, similiar to the idea of representing words a vectors (Google's word2vec)
3. we need a fast parallel implementation

## TODO
examples 

# python wrapper for sequitur

## Idea
1. sequitur will be used as the context-free grammar extractor for SAXed data
2. the mined rules will be used for outlier/motif detection 
3. we wrap the [c++ implementation](http://sequitur.info/latest/sequitur.tgz) for python usage - so it is just a quick workaround for now.

## References
1. [three papers listed on Grammarviz website](http://grammarviz2.github.io/grammarviz2_site/)
2. [sequitur site](http://www.sequitur.info/)
3. [another python sequitur implementation](http://www.hcs.harvard.edu/saagar/parallel-sequitur/web/program.php)
4. [java implementation](https://github.com/GrammarViz2/grammarviz2_src) can be found in grammarviz2 implementation

## how to use the wrapper
1. download c++ code http://sequitur.info/latest/sequitur.tgz
2. put the `sequitur` code from the uncompressed folder in a convienet place
3. use the pysequitur package and pass the path to `sequitur` as constructor parameter

## why do we wrap it?
1. to make it easier to use with pysax
2. we understand that the c++ implementation treats rule terminals as single characters, whereas in pysax we are dealing with words, so we need to map the words to single characters first - this might change in future based on our understanding of the code.

## TODO
examples
