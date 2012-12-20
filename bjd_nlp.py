
import matplotlib.pyplot as plt
import nltk
import numpy as np
import re


################################################################################
def remove_non_ascii(s) :
    """Removes all non-ascii characters from input string.
    """
    return "".join(c for c in s if ord(c)<128)


################################################################################
def remove_URLs(s) :
    """Removes all URLs from input string.
    """
    pattern = r'((http|ftp|https):\/\/)?[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    return re.sub(pattern, ' ', s)


################################################################################
def clean_text(text) :
    """Removes digits, non-standard white space, URLs, and non-Ascii from raw text.
    """
    text = text.lower()              # remove capitalization
    text = re.sub('\d', ' ', text)   # remove digits
    text = re.sub('\s+', ' ', text)  # standardize white space
    text = remove_URLs(text)         # remove all urls
    text = remove_non_ascii(text)    # remove all non-ascii characters
    return text


################################################################################
def stem_words(words, which='porter') :
    """Given a list of words (tokenized), return list of stemmed words
    @param which: Which stemmer to use, either porter or lancaster
    @type which: string
    """
    if which.lower() == 'porter' :
        stemmer = nltk.PorterStemmer()
    elif which.lower() == 'lancaster' :
        stemmer = nltk.LancasterStemmer()
    else :
        raise NameError("'which' argument must have value of 'porter' or 'lancaster'")
    stems = [stemmer.stem(word) for word in words]
    return stems


################################################################################
def tokenize_and_tag(text) :
    """Given text (string), tokenize into sentences and words and tag parts-of-spech.
    """
    sents = nltk.sent_tokenize(text)    # default sentence tokenizer
    sents = [nltk.wordpunct_tokenize(sent) for sent in sents]    # default word tokenizer
    sents = [nltk.pos_tag(sent) for sent in sents]    # default POS tagger
    return sents


################################################################################
def get_nbest_trigrams(words, measure='pmi', min_freq=0, stop_ngs=[], n_best=10, scores=False) :
    """Gets N best trigrams from a list of words.
    @param measure: ngram association measure to use in scoring
    @type measure: string; 'pmi', 'chi_sq', 'likelihood_ratio', 'student_t', 'raw_freq'
    @param min_freq: minimum ngram frequency to keep
    @type min_freq: int; default value of 0, so no frequency filtering
    @param n_best: number of highest-scored ngrams to return
    @param stop_ngs: list of ngrams to remove from consideration
    @type stop_ngs: list
    @type n_best: int
    @param scores: return tuples of ngram and scores, or not
    @type scores: boolean
    """
    tcf = nltk.collocations.TrigramCollocationFinder.from_words(words)
    tcf.apply_word_filter(lambda w: len(w) < 3 or w in set(nltk.corpus.stopwords.words('english')))
    tcf.apply_ngram_filter(lambda w1, w2, w3: ' '.join([w1,w2,w3]) in stop_ngs)
    tcf.apply_freq_filter(min_freq)
    if measure == 'pmi' : m = nltk.collocations.TrigramAssocMeasures.pmi
    elif measure == 'chi_sq' : m = nltk.collocations.TrigramAssocMeasures.chi_sq
    elif measure == 'likelihood_ratio' : m = nltk.collocations.TrigramAssocMeasures.likelihood_ratio
    elif measure == 'student_t' : m = nltk.collocations.TrigramAssocMeasures.student_t
    elif measure == 'raw_freq' : m = nltk.collocations.TrigramAssocMeasures.raw_freq
    else : raise NameError('Valid association measure must be provided!')
    if scores is False :
        return tcf.nbest(m, n_best)
    elif scores is True :
        return tcf.score_ngrams(m)[:n_best]


################################################################################
def get_nbest_bigrams(words, measure='pmi', min_freq=0, stop_ngs=[], n_best=10, scores=False) :
    """Gets N best bigrams from a list of words.
    @param measure: ngram association measure to use in scoring
    @type measure: string; 'pmi', 'chi_sq', 'likelihood_ratio', 'student_t', 'raw_freq'
    @param min_freq: minimum ngram frequency to keep
    @type min_freq: int; default value of 0, so no frequency filtering
    @param n_best: number of highest-scored ngrams to return
    @param stop_ngs: list of ngrams to remove from consideration
    @type stop_ngs: list
    @type n_best: int
    @param scores: return tuples of ngram and scores, or not
    @type scores: boolean
    """
    bcf = nltk.collocations.BigramCollocationFinder.from_words(words)
    bcf.apply_word_filter(lambda w: len(w) < 3 or w in set(nltk.corpus.stopwords.words('english')))
    bcf.apply_ngram_filter(lambda w1, w2: ' '.join([w1,w2]) in stop_ngs)
    bcf.apply_freq_filter(min_freq)
    if measure == 'pmi' : m = nltk.collocations.BigramAssocMeasures.pmi
    elif measure == 'chi_sq' : m = nltk.collocations.BigramAssocMeasures.chi_sq
    elif measure == 'likelihood_ratio' : m = nltk.collocations.BigramAssocMeasures.likelihood_ratio
    elif measure == 'student_t' : m = nltk.collocations.BigramAssocMeasures.student_t
    elif measure == 'raw_freq' : m = nltk.collocations.BigramAssocMeasures.raw_freq
    else : raise NameError('Valid association measure must be provided!')
    if scores is False :
        return bcf.nbest(m, n_best)
    elif scores is True :
        return bcf.score_ngrams(m)[:n_best]


################################################################################
def regex_chunker(sentence, np_only=False) :
    """Given POS-tagged sentence, returns tree with chunked phrases.
    @param sentence: Tokenized sentence with tagged parts of speech (NLTK)
    @param np_only: look only for NPs (and not PPs or VPs)
    @type np_only: boolean
    """
    if np_only is False :
        grammar = r"""
            NP: {<DT|PP\$>?<JJ>*<NN>} # determiner/possessive, adjectives, and noun
                {<NN.*>+}             # consecutive (proper) nouns
            PP: {<IN><NP>}            # preposition + NP
            VP: {<VB.*><NP|PP>*}      # verb words + NPs or PPs
            """
    elif np_only is True :
        grammar = r"""
            NP: {<DT|PP\$>?<JJ>*<NN>} # determiner/possessive, adjectives, and noun
                {<NN.*>+}             # consecutive (proper) nouns
            """
    cp = nltk.RegexpParser(grammar, loop=2)
    tree = cp.parse(sentence)
    return tree


################################################################################
def plot_freq_dist(fd, ylim=20, title=False) :
    """Plots NLTK FreqDist in slightly nicer format
    @param fd: Frequency distribution (NLTK)
    @param title: Name of title to add to freq dist
    @type title: string, or boolean False by default
    @param ylim: Number of entries on y-axis
    @type ylim: int
    """
    fig = plt.figure("fd", figsize=(6,12), dpi=300, facecolor='white', edgecolor='white')
    ax = fig.add_subplot(1,1,1)
    plt.subplots_adjust(left=0.25, right=0.9, top=0.9, bottom=0.1)
    if title is not False : ax.set_title(title)
    plot = ax.plot([fd[key] for key in fd.keys()], range(0, len(fd.keys())),
    linewidth=10, color='red')
    y_ticks = []
    y_ticklabels = []
    for i, label in enumerate(fd.keys()) :
        y_ticks.append(i)
        y_ticklabels.append(label)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_ticklabels)
    ax.set_ylim(0,ylim)
    ax.set_xlim(0, fd[fd.keys()[0]]+1)
    ax.set_xlabel('Number of Articles with Mention')
    plt.gca().invert_yaxis()
    plt.show()


################################################################################
def plot_barh_chart(fd, ylim=20, title=False, xlab='Default xlab',
                    n_docs=0, save=False) :
    """Plots word frequency distribution (NLTK) as horizontal bar chart.
    @param fd: Frequency distribution (NLTK)
    @param title: Name of title to add to bar chart
    @type title: string, or boolean False by default
    @param ylim: Number of bars on y-axis
    @type ylim: integer
    @param n_docs: Plot bar lengths as fraction of total documents
    @type n_docs: integer
    @param save: Save plot instead of showing it.
    @type save: boolean False by default
    """
    fig = plt.figure("fd", figsize=(10,6), dpi=150, facecolor='white', edgecolor='white')
    ax = fig.add_subplot(1,1,1)
    plt.subplots_adjust(left=0.25, right=0.9, top=0.9, bottom=0.1)
    if title is not False : ax.set_title(title)
    ax.set_xlabel(xlab)
    pos = np.arange(ylim)+0.5
    if n_docs == 0 :
        lengths = np.array(fd.values()[0:ylim])
        ax.set_xlim(0, fd[fd.keys()[0]]+1)
    else :
        lengths = np.array(fd.values()[0:ylim]) / float(n_docs)
        ax.set_xlim(0, np.array(fd[fd.keys()[0]]+1) / float(n_docs))
    rects = ax.barh(pos, lengths, align='center', color='CornflowerBlue', linewidth=0)
    ax.set_yticks(pos)
    ax.set_yticklabels(fd.keys())
    ax.yaxis.set_ticks_position('none')
    ax.get_xaxis().tick_bottom()
    for spine in ['left', 'right', 'top'] :
        ax.spines[spine].set_visible(False)
    ax.set_ylim(-0.5, ylim)
    plt.gca().invert_yaxis()
    if save is False :
        plt.show()
    elif save is True :
        plt.savefig('plot_barh_chart.pdf', dpi=300)






