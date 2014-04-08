import json, cPickle
import scipy as sp
import numpy as np


tf = TfidfTransformer()
X = tf.fit_transform(counts.toarray())


def load_files(statelist):
    import cPickle

    root = '/Users/amentch/code/zipfian/project/states/pickles2/'
    suffixes = ['_clean.pkl','_cv.pkl','_counts.pkl', '_tfidf.pkl', '_transformed_tfidf.pkl']

    st_dict = {st: {} for st in statelist}
    for st in statelist:
        for suf in suffixes:
            with open(root + st + suf, 'rb') as f:
                temp = cPickle.load(f)
            st_dict[st][suf.strip('_').split('.')[0]] = temp
        print st

    all_data = {}

    return st_dict

def pre_gensim(st_dict):
    states = st_dict.keys()
    tokened = {}
    for st in states:
        tokened.update({x: st_dict[st]['clean'][x].split() for x in st_dict[st]['clean']})

    billids = []
    texts = []
    for item in tokened.items():
        billids.append(item[0])
        texts.append(item[1])

    return tokened, billids, texts

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('subset_corpus.mm', corpus)

class MyCorpus(object):
    def __iter__(self):
        for line in open('corpus.txt'):
            yield dictionary.doc2bow(line.lower().split())

dictionary = corpora.Dictionary(line for line in open('corpus.txt'))
corpus = corpora.MmCorpus('/Users/amentch/code/zipfian/project/states/pickles2/subset_corpus.mm')
tfidf = models.TfidfModel(corpus)


def stemmed_texts(st_dict):
    proc_texts = {st: {} for st in st_dict.keys()}
    for st in st_dict.keys():
        with open(st + '_cv.pkl','rb') as f:
            cv = cPickle.load(f)
        with open(st + '_counts.pkl','rb') as f:
            counts = cPickle.load(f)
        rev_idx = {cv.vocabulary_[x]: x for x in cv.vocabulary_}
        for idx, billid in enumerate(st_dict[st]['clean']):
            proc_texts[st][billid] = []
            for i in counts[idx].nonzero()[1]:
                proc_texts[st][billid].append(rev_idx[i])
            # proc_texts[st][billid] = ' '.join(proc_texts[st][billid])

    return proc_texts


alltexts = {}
for st in proc_texts.keys():
    for billid in proc_texts[st].keys():
        alltexts[billid] = proc_texts[st][billid]

alldict = corpora.Dictionary(alltexts.values())

corpus = [alldict.doc2bow(bill) for bill in alltexts.values()]

all_lda = models.LdaModel(corpus, id2word=alldict, num_topics=500)

clustered = all_lda[alltexts.values()]

topics = []
failed = []
counter = 0
for doc in clustered:
    try:
        topics.append({idx: n[0] for idx, n in enumerate(heapq.nlargest(3, doc, key=lambda x: x[1]))})
    except:
        topics.append(-1)
        failed.append(counter)
    counter += 1

def build_cluster(topic_num, topic_list, bill_lookup):
    cluster = [bill_lookup[idx] for idx, i in enumerate(topic_list) for j in i if j == topic_num]
    return cluster


alltopics = []
for doc in clustered:
    try:
        alltopics.append([x[0] for x in doc])
    except:
        alltopics.append(-1)

