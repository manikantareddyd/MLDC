# Mulit-Lingual Document Clustering

### Using the wikipedia extractor
  + Usage: python src/getDocFromWiki.py <Article Name>
  + Note: <Article Name> should have a valid wikipedia page accessible at http://en.wikipedia.org/wiki/<Article Name>. The page should never lead to disambiguation.
  + Example: 'python src/getDocFromWiki.py India'

### Semantic Clustering

The current method present in src/freqModel, uses a frequency distribution model to vectorize words with topics as coordinates. In this Topic Based Hyper space, it is expected that semantically similar words group together.

So we generate clusters in this vector space, Note that the dimensionality of this space depends on the number of topics we choose.

Once the semantics clusters are obtained, we generate frequency of the words of a given cluster that appear in a given document. By using this cluster frequency we generate vectors for every document of dimensionality equal to number of semantic clusters generated.

This vector representation of documents has proven to be good so far.     

### Update: The below method is Depreciated  
This is a word frequency scatter across english and french for
Physics, Chemistry and politcs?

There is a very strong necessity of playing with frequency normalization functions (Term frequency functions log or idf are good too)
So far exp and log have displayed very good potential
also Distance norms are to be experimented
