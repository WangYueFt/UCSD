wordDict = {}
with open("hw1_word_count_05.txt", 'r') as file:
    for line in file:
        line = line.upper().strip().split(' ')
        wordDict[line[0]] = float(line[1])
print sorted(wordDict.items(), key=lambda x: x[1])[0:8]
print sorted(wordDict.items(), key=lambda x: x[1], reverse=True)[0:8]