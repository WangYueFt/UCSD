import string
import sys
class Hangman():
	def __init__(self, fileNum):
		wordDict = {}
		totalCount = 0
		if int(fileNum) < 10:
			fileNum = 0 + str(fileNum)
		filename = "hw1_word_count_" + fileNum + ".txt"
		with open(filename, 'r') as file:
		    for line in file:
		        line = line.upper().strip().split(' ')
		       	wordDict[line[0]] = float(line[1])
		      	totalCount += int(line[1])
		wordDict = dict(map(lambda x: (x[0], x[1]/totalCount), wordDict.items()))
		self.wordDict = wordDict
		self.alphabeta = string.uppercase
		
	def outputFreq(self):
		wordDict = self.wordDict
		mostFreq = sorted(wordDict.items(), key = lambda x: x[1])[-1:-9:-1]
		leastFreq = sorted(wordDict.items(), key = lambda x: x[1])[0:8]
		print mostFreq
		print leastFreq

	def conditionalProb(self, word):
		corrGuessed = self.corrGuessed
		inCorrGuessed = self.inCorrGuessed
		alphabeta = self.alphabeta
		cond = {}
		for i in range(26):
			c = alphabeta[i]
			if c not in corrGuessed and c not in inCorrGuessed and c in word:
			 	cond[c] = 1
			# for i in range(len(word)):
			# 	if corrGuessed[i] == ' ' and word[i] == c:
			# 		cond[c] = 1
			# 		break
			else:
				cond[c] = 0
		return cond

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

	def pred4i(self, postProbDict, condProbDict, c):
		prob = 0.0
		for key in postProbDict.keys():
			prob += postProbDict[key]*condProbDict[key][c]
		return prob

	def predictiveProb(self, corrGuessed, inCorrGuessed):
		self.corrGuessed = corrGuessed
		self.inCorrGuessed = inCorrGuessed
		wordDict = self.wordDict
		alphabeta = self.alphabeta
		prob = {}
		postProbDict = self.posteriorProb()
		condProbDict = dict(map(lambda x: (x, self.conditionalProb(x)), wordDict.keys()))
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

