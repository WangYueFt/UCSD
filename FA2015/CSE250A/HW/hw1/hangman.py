import string
import sys
#Usage instruction:
#Python hangman.py [word length] [correctly guessed(don't leave out the space)] [incorrectly guessed]

class Hangman():

	#This function is to load the corresponding corpora and load the correctly guessed word
	#and incorrectly guessed word.
	#And calculating word frequence.

	def __init__(self, fileNum):
		wordDict = {}
		totalCount = 0
		if int(fileNum) < 10:
			fileNum = '0' + str(fileNum)
		filename = "hw1_word_count_" + fileNum + ".txt"
		with open(filename, 'r') as file:
		    for line in file:
		        line = line.upper().strip().split(' ')
		       	wordDict[line[0]] = float(line[1])
		      	totalCount += int(line[1])
		wordDict = dict(map(lambda x: (x[0], x[1]/totalCount), wordDict.items()))
		self.wordDict = wordDict
		self.alphabeta = string.uppercase

	#This function is to output the most frequent words and the least frequent words. 

	def outputFreq(self):
		wordDict = self.wordDict
		mostFreq = sorted(wordDict.items(), key = lambda x: x[1])[-1:-9:-1]
		leastFreq = sorted(wordDict.items(), key = lambda x: x[1])[0:8]
		print mostFreq
		print leastFreq

	#This function is to calculate the probability of evidence E given the word W. 

	def conditionalProb(self, word):
		corrGuessed = self.corrGuessed
		inCorrGuessed = self.inCorrGuessed
		alphabeta = self.alphabeta
		cond = {}
		for i in range(26):
			c = alphabeta[i]
			#If the c is the next right letter in the word.
			if c not in corrGuessed and c not in inCorrGuessed and c in word:
			 	cond[c] = 1
			else:
				cond[c] = 0
		return cond

	#This function is to test whether the word and the evidence is compatible.

	def compatible(self, word):
		corrGuessed = self.corrGuessed
		inCorrGuessed = self.inCorrGuessed
		for i in range(len(corrGuessed)):
			if corrGuessed[i] != ' ':
				if corrGuessed[i] != word[i]:
					return False
			else:
				if word[i] in corrGuessed or word[i] in inCorrGuessed:
					return False
		return True

	#This function is to compute the posterior probability of a word given evidence E.

	def posteriorProb(self):
		corrGuessed = self.corrGuessed
		inCorrGuessed = self.inCorrGuessed
		wordDict = self.wordDict
		postProbDict = {}
		denominator = 0.0
		for key in wordDict:
			singProb = wordDict[key] * (1 if self.compatible(key) else 0)
			denominator += singProb
			postProbDict[key] = singProb
		
		postProbDict = dict(map(lambda x: (x[0], x[1]/denominator), postProbDict.items()))
		return postProbDict

	#Calculate and then sumarize all the predictive probability of a leter through all words.

	def pred4i(self, postProbDict, condProbDict, c):
		prob = 0.0
		for key in postProbDict.keys():
			prob += postProbDict[key]*condProbDict[key][c]
		return prob

	#This function is to give the predictive probabilities of 26 leters.

	def predictiveProb(self, corrGuessed, inCorrGuessed):
		self.corrGuessed = corrGuessed
		self.inCorrGuessed = inCorrGuessed
		wordDict = self.wordDict
		alphabeta = self.alphabeta
		prob = {}
		#Calculate the posterior probability
		postProbDict = self.posteriorProb()
		#Calculate the conditional probability
		condProbDict = dict(map(lambda x: (x, self.conditionalProb(x)), wordDict.keys()))
		#Use product rule and marginiztion to get the final predictive probability.
		prob = dict(map(lambda x: (x, self.pred4i(postProbDict, condProbDict, x)), alphabeta))
		return prob
		

def main():
		
	wordLen = sys.argv[1]
	corrGuessed = sys.argv[2]
	inCorrGuessed = sys.argv[3]
	
	h = Hangman(wordLen)

	h.outputFreq()

	prob = h.predictiveProb(corrGuessed, inCorrGuessed)
	print sorted(prob.items(), key=lambda x: x[1])

if __name__ == '__main__':
	main()

