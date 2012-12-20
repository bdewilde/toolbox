
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
    @type: string
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
def regex_chunker(sentence, np_only=False) :
    """Given POS-tagged sentence, returns tree with chunked phrases.
    @param sentence: Tokenized sentence with tagged parts of speech (NLTK)
    @param np_only: look only for NPs (and not PPs or VPs)
    @type: boolean
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
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(sentence)
    return tree


################################################################################
def plot_freq_dist(fd, ylim=20, title=False) :
    """Plots NLTK FreqDist in slightly nicer format
    @param fd: Frequency distribution (NLTK)
    @param title: Name of title to add to freq dist
    @type string, or boolean False by default
    @param ylim: Number of entries on y-axis
    @type: integer
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
def plot_barh_chart(fd, ylim=20, title=False,
                    frac=False, save=False) :
    """Plots word frequency distribution (NLTK) as horizontal bar chart.
    @param fd: Frequency distribution (NLTK)
    @param title: Name of title to add to bar chart
    @type: string, or boolean False by default
    @param ylim: Number of bars on y-axis
    @type: integer
    @param frac: Plot bar lengths as fraction of total documents
    @type: boolean False by default
    @param save: Save plot instead of showing it.
    @type : boolean False by default
    """
    fig = plt.figure("fd", figsize=(10,6), dpi=150, facecolor='white', edgecolor='white')
    ax = fig.add_subplot(1,1,1)
    plt.subplots_adjust(left=0.25, right=0.9, top=0.9, bottom=0.1)
    if title is not False : ax.set_title(title)
    pos = np.arange(ylim)+0.5
    if frac is False :
        lengths = np.array(fd.values()[0:ylim])
        ax.set_xlabel('Number of Articles with Mention')
        ax.set_xlim(0, fd[fd.keys()[0]]+1)
    elif frac is True :
        lengths = np.array(fd.values()[0:ylim]) / float(numDocs)
        ax.set_xlabel('Fraction of Articles with Mention')
        ax.set_xlim(0, np.array(fd[fd.keys()[0]]+1)/ float(numDocs))
    rects = ax.barh(pos, lengths, align='center', color='CornflowerBlue', linewidth=0)
    ax.set_yticks(pos)
    ax.set_yticklabels(fd.keys())
    ax.yaxis.set_ticks_position('none')
    ax.set_ylim(-0.5, ylim)
    plt.gca().invert_yaxis()
    if save is False :
        plt.show()
    elif save is True :
        plt.savefig('plot_barh_chart.pdf', dpi=300)