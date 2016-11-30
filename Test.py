from __future__ import division

import Util

def vectorize(a,b):
    dictionary = list(set(a) | set(b))
    v1 = [0]*len(dictionary)
    v2 = [0]*len(dictionary)
    for aa in a:
        idx = dictionary.index(aa)
        v1[idx] = 1

    for bb in b:
        idx = dictionary.index(bb)
        v2[idx] = 1
    return v1,v2

def calculatePrecision(tn, tp, fn, fp):
    if tp + fp == 0:
        pr = 0
    else:
        pr = tp / (tp + fp)
    return pr

def calculateRecall(tn, tp, fn, fp):
    if tp + fn == 0:
        rec = 0
    else:
        rec = tp / (tp + fn)
    return rec

def calculateFmeasure(pr, rec):
    if pr + rec == 0:
        fm = 0
    else:
        fm = 2 * pr * rec / (pr + rec)
    return fm

def calculateAccuracy(tn, tp, fn, fp):
    if tp + tn + fp + fn == 0:
        ac = 0
    else:
        ac = (tp + tn) / (tp + tn + fp + fn)
    return ac

def calculateMetrics(a,b):
    tn, tp, fn, fp = 0, 0, 0, 0
    for i in range(0,len(a)):
        aa = a[i]
        bb = b[i]
        if aa == 0 and bb == 0:
            tn += 1
        elif aa == 0 and bb == 1:
            fp += 1
        elif aa == 1 and bb == 0:
            fn += 1
        elif aa == 1 and bb == 1:
            tp += 1
        else:
            print "entrou no else"

    precision = calculatePrecision(tn, tp, fn, fp)
    recall = calculateRecall(tn, tp, fn, fp)
    accuracy = calculateAccuracy(tn, tp, fn, fp)
    fmeasure = calculateFmeasure(precision, recall)
    return {'precision':precision, 'recall':recall, 'accuracy':accuracy, 'f-measure':fmeasure}

## so p testar
def process(document):
    return document.links

# a = [('a',21),('b',43),('c',23),('d',30),('e',45)] # ground truth
# b = [('a',0),('d',30),('e',45),('f',21)]           # estimate
# v1, v2 = vectorize(a,b)
# metrics = calculateMetrics(v1,v2)
# print metrics

# read all pages in the database
database = Util.getWikipediaPages()

print "Size of the database: ", len(database), "\n"

total_accuracy = []
total_precision = []
total_recall = []
total_fmeasure = []

for document in database:
    # process eh a funcao que vai fazer tudo e devolver os links
    # os links serao devolvidos do mesmo jeito que os links do objeto
    true_links = document.links
    estimated_links = process(document)

    v1, v2 = vectorize(true_links, estimated_links)
    metrics = calculateMetrics(v1, v2)

    print document.title, metrics

    total_accuracy.append(metrics['accuracy'])
    total_precision.append(metrics['precision'])
    total_recall.append(metrics['recall'])
    total_fmeasure.append(metrics['f-measure'])

accuracy = sum(total_accuracy) / len(total_accuracy)
precision = sum(total_precision) / len(total_precision)
recall = sum(total_recall) / len(total_recall)
fmeasure = sum(total_fmeasure) / len(total_fmeasure)

print "\nMedia macro das medidas"
print "\tAccuracy: ", accuracy
print "\tPrecision: ", precision
print "\tRecall: ", recall
print "\tF-measure: ", fmeasure
