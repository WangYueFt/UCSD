import math
import sys
import numpy as np
import pylab
import matplotlib.ticker as ticker
vocabs = {}
rvocabs = {}
#Readin the vocabulary
with open('hw3_vocab.txt', 'r') as f_vocab:
	i = 1
	for line in f_vocab:
		line = line.strip()
		vocabs[i] = line
		rvocabs[line] = i
		i += 1
unigrams = {}
n = 0
#readin unigram
with open('hw3_unigram.txt', 'r') as f_uni:
	i = 1
	for line in f_uni:
		line = line.strip()
		unigrams[vocabs[i]] = int(line)
		i = i + 1
		n += int(line)
toprint = []
#calculate the unigram probabilities of words that start with 'M'
for key in unigrams.keys():
	#unigrams[key] = float(unigrams[key])/n
	if key[0] == 'M':
		toprint.append((key, float(unigrams[key])/n))
#output
c = 1
for x, y in sorted(toprint, key=lambda x: x[1],reverse=True):
	print c,':', x, y
	c = c+1
bigrams = {}
bigrams_all = {}
#readin the bigram and output the bigram probabilities of words that follow 'THE'
with open('hw3_bigram.txt', 'r') as f_bi:
	for line in f_bi:
		line = line.strip().split('\t')
		bigrams_all[int(line[0])*1000+int(line[1])] = float(line[2])
		# if int(line[0]) == rvocabs['THE']:
			# bigrams[line[1]] = float(line[2])/unigrams['THE']
# top10 = map(lambda x:(vocabs[int(x[0])], x[1]), sorted(bigrams.items(), key=lambda x: x[1], reverse=True)[0:10])
# for x, y in top10:
		# print x, y
#Calculate the unigram log-likelihood probabilities
print unigrams
print bigrams_all
def uniprob(sentence, unigrams):
	p_uni = 1.0
	for word in sentence.split(' '):
		p_uni *= (float(unigrams[word])/n)
	return math.log(p_uni)
#Calculate the bigram log-likelihood probabilities
def biprob(bi_sentence, unigrams, bigrams_all, rvocabs):
	bi_sentence = bi_sentence.split(' ')
	p_bi = 1.0
	isOb = False;
	for i in xrange(1, len(bi_sentence), 1):
		prev = bi_sentence[i-1]
		now = bi_sentence[i]
		if rvocabs[prev]*1000+rvocabs[now] not in bigrams_all.keys():
			print prev, now
			isOb = True;
		else:
			p_bi = p_bi*(bigrams_all[rvocabs[prev]*1000+rvocabs[now]]/unigrams[prev])
	if isOb:
		return math.log(sys.float_info.min)
	else:
		return math.log(p_bi)
#Calculate the log-likelihood probabilities using mix model
def mixprob(sentence, unigrams, bigrams_all, rvocabs, lam):
 	bi_sentence = '<s> ' + sentence
 	#sentence = sentence.split(' ')
 	bi_sentence = bi_sentence.split(' ')
 	p_mix = 1.0
 	for i in xrange(1, len(bi_sentence), 1):
 		prev = bi_sentence[i-1]
 		now = bi_sentence[i]
 		uni = float(unigrams[now])/n
 		if rvocabs[prev]*1000+rvocabs[now] not in bigrams_all.keys():
 			p_mix = p_mix * (lam*uni)
 		else:
 			bi = (bigrams_all[rvocabs[prev]*1000+rvocabs[now]]/unigrams[prev])
 			p_mix = p_mix * (lam*uni+(1.0-lam)*bi)
 	return math.log(p_mix)
sentence = 'a a a a b b b b c c c c d d d d a a a a'
sentence = sentence.upper()
print uniprob(sentence, unigrams)
print biprob(sentence, unigrams, bigrams_all, rvocabs)
# sentence = 'The stock market fell by one hundred points last week'
# sentence = sentence.upper()
# print uniprob(sentence, unigrams)
# bi_sentence = '<s> ' + sentence
# print biprob(bi_sentence, unigrams, bigrams_all, rvocabs)

# sentence = 'The sixteen officials sold fire insurance'
# sentence = sentence.upper()
# print uniprob(sentence, unigrams)
# bi_sentence = '<s> ' + sentence
# print biprob(bi_sentence, unigrams, bigrams_all, rvocabs)

# lams = []
# probs = []
# #Generate the function samples
# for i in np.arange(0.64000, 0.66000, 0.00001):
# 	lams.append(i)
# 	probs.append(mixprob(sentence, unigrams, bigrams_all, rvocabs, i))
# 	print i
# #Plot the log-likelihood as the function of lambda
# pylab.figure()
# ax = pylab.gca()
# ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.5))
# ax.yaxis.grid(True, which='minor')
# ax.yaxis.set_ticks_position('both')
# ax.xaxis.set_major_locator(ticker.MultipleLocator(0.2))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.05))
# ax.xaxis.grid(True, which='minor')
# plt = pylab.plot(lams[1000:], probs[1000:])
# pylab.ylabel('Log-Likelihood')
# pylab.xlabel('Lambda')
# pylab.show()
# print lams[probs.index(max(probs))]
