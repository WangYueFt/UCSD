f = open("hw1_word_count_10.txt", "r")
P = dict()
wordLength = 10
total = 0
for line in f:
    lineContent = line.split()
    word = lineContent[0]
    count = int(lineContent[1])
    if P.get(word) != None:
        P[word] += count
    else:
        P[word] = count
    total += count

for key in P:
    P[key] = 1.0 * P[key] / total

correctGuessInput = raw_input("Input correctly guessed String:")
wrongGuessInput = raw_input("Input incorrectly guessed String:")

correctGuess = correctGuessInput
allGuess = []
wrongGuess = []
for char in wrongGuessInput:
    if char.isalpha():
        allGuess.append(char)
        wrongGuess.append(char)
for char in correctGuessInput:
    if char.isalpha():
        allGuess.append(char)

guess = [0] * 26

cache = dict()
cachesum = 0

for word in P:
    smallP = P[word]
    for i in xrange(wordLength):
        if correctGuess[i] != "-":
            if correctGuess[i] != word[i]:
                smallP = 0
                break
        else:
            if word[i] in allGuess:
                smallP = 0
                break
    cache[word] = smallP
    cachesum += smallP
print sorted(cache.items(), key=lambda x: x[1])
print cachesum
exit()
for index in xrange(26):
    myguess = chr(index + 65)
    pSum = 0
    if myguess in allGuess:
        continue
    for word in P:
        right = 0
        left = 0
        for i in xrange(wordLength):
            if correctGuess[i] == "-" and word[i] == myguess:
                right = 1
                break
        if right == 0:
            pSum += 0
        else:
            numerator = cache[word]
            denominator = cachesum
            pSum += 1.0 * numerator / denominator
    guess[index] = pSum

print guess
print max(guess)
print chr(guess.index(max(guess)) + 65)
