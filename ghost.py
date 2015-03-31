#ghost
import random

alphabet = 'etaoinshrdlcumwfgypbvkjxqz'
game = 'Ghost'
RANDOMNESS = 0.5

def runGame():
	print('Hard game? "y" or "n"')
	difficulty = raw_input()
	if difficulty == 'y':
		gametrie = checktrie
	else:
		gametrie = trie
	humanScore = 0
	compScore = 0
	turn = False
	print('Hello player, prepare for defeat.')
	print('Type "?" to challenge.  Turns will alternate.')
	while humanScore < 5 and compScore < 5:
		if runRound(gametrie, turn) == 1:
			humanScore += 1
		else:
			compScore += 1
		turn = not turn
		print('You have "' + game[:humanScore] + '" and the computer has "' + game[:compScore] + '"')
	if humanScore == 5:
		print('YOU LOSE')
	else:
		print('YOU WIN')



def runRound(trie, turn):
	word = ''
	challenge = 0
	human = True
	if turn:
		word = alphabet[random.randrange(25)]
		print('Computer starts and chooses "' + word +'"')
	while(challenge < 2 and not isWord(word)):
		if human:
			word, challenge = humanTurn(word, challenge)
			human = False
		else:
			word, challenge = compTurn(trie, word, challenge)
			human = True
	if challenge == 2:
		print('Congratulations!  You have defeated the computer with the word "' + word + '"')
		return 0
	elif challenge == 3:
		print('Sorry, the computer defeated you with the word "' + word + '"')
		return 1
	elif human:
		print('Congratulations!  You have defeated the computer with the word "' + word + '"')
		return 0
	else:
		print('Sorry, the computer defeated you with the word "' + word + '"')
		return 1

def humanTurn(word, challenge):
	print('The current letters are "' + word + '"')
	if challenge == 1:
		print('You have been challenged, please type a full word.')
		#human input
		newWord = raw_input()
		if startsWith(word, newWord) and isWord(newWord):
			challenge = 2
			word = newWord.lower()
		else:
			print('Invalid word.')
			challenge = 3
	else:
		print('Please add 1 letter.')
		letter = raw_input()
		while(len(letter) != 1):
			print('Invalid letter, try again.')
			letter = raw_input()
		if letter == '?':
			challenge = 1
		else:
			word += letter.lower()
	return word, challenge

def compTurn(trie, word, challenge):
	#change trie to checktrie for harder play
	if challenge == 1:
		if in_trie_weak(trie, word):
			return finishWord(trie, word), 3
		else:
			return word, 2
	if not more_trie(trie, word):
		return word, 1
	newLetter = endChoose(trie, word)
	print('Computer chooses ' + newLetter)
	if newLetter == '':
		return word, 1
	return word + newLetter, challenge

def restrictChoose(trie, word):
	#chooses one with fewest options
	biggest = 30
	bestLetter = alphabet[random.randrange(5)]
	temp_trie = findTrie(trie, word)
	for key in temp_trie.keys():
		if len(temp_trie[key]) < biggest and "_end_" not in temp_trie[key]:
			biggest = len(temp_trie[key])
			bestLetter = key
	return bestLetter

def optionChoose(trie, word):
	#chooses one with most options
	biggest = 0
	bestLetter = alphabet[random.randrange(5)]
	temp_trie = findTrie(trie, word)
	for key in temp_trie.keys():
		if len(temp_trie[key]) > biggest and "_end_" not in temp_trie[key]:
			biggest = len(temp_trie[key])
			bestLetter = key
	return bestLetter

def randChoose(trie, word):
	temp_trie = findTrie(trie, word)
	options = []
	for key in temp_trie.keys():
		if '_end_' not in temp_trie[key]:
			options.append(key)
	if len(options) == 0:
		if random.random() < RANDOMNESS:
			return alphabet[random.randrange(5)]
		return ''
	return random.choice(options)

def endChoose(trie, word):
	#choose a forced win if possible
	temp_trie = findTrie(trie, word)
	for key in temp_trie.keys():
		check = temp_trie[key]
		if '_end_' not in check:
			if len(check) == 1 and check.keys()[0] == '_end_':
				return key 
	return randChoose(trie, word)

def weightedChoose(trie, word):
	if random.random() < RANDOMNESS:
		return alphabet[random.randrange(5)]
	return smartChoose(trie, word)

def startsWith(word, newWord):
	if len(word) == 0:
		return True
	if len(word) > len(newWord):
		return False
	if word[0] != newWord[0]:
		return False
	return startsWith(word[1:],newWord[1:])

def isWord(word):
	if len(word) < 4:
		return False
	return in_trie(checktrie, word)


def finishWord(trie, word):
	temp_trie = findTrie(trie, word)
	while "_end_" not in temp_trie:
		keys = temp_trie.keys()
		word = word + keys[0]
		temp_trie = temp_trie[keys[0]]
	return word



def make_trie(wordList):
    """
    Make a trie by given words.
    """
    trie = {}
 
    for word in wordList:
        if type(word) != str:
            raise TypeError("Trie only works on str!")
        temp_trie = trie
        for letter in word:
            temp_trie = temp_trie.setdefault(letter, {})
        temp_trie = temp_trie.setdefault('_end_', '_end_')
 
    return trie
 
 
def in_trie(trie, word):
    """
    Detect if word in trie.
    """
    if type(word) != str:
        raise TypeError("Trie only works on str!")
 
    temp_trie = trie
    for letter in word:
        if letter not in temp_trie:
            return False
        temp_trie = temp_trie[letter]

    if "_end_" in temp_trie:
    	return True
    else:
    	return False

def in_trie_weak(trie, word):
    """
    Detect if word in trie.
    """
    if type(word) != str:
        raise TypeError("Trie only works on str!")
 
    temp_trie = trie
    for letter in word:
        if letter not in temp_trie:
            return False
        temp_trie = temp_trie[letter]
    return True

def more_trie(trie, word):
    """
    Detect if more word in trie.
    """
    if type(word) != str:
        raise TypeError("Trie only works on str!")
 
    temp_trie = trie
    for letter in word:
        if letter not in temp_trie:
            return False
        temp_trie = temp_trie[letter]
    return temp_trie.keys()[0] != '_end_' or len(temp_trie.keys()) > 1 

def findTrie(trie, string):
	temp_trie = trie
	for letter in string:
		if letter not in temp_trie:
			return {}
		temp_trie = temp_trie[letter]
	return temp_trie
 

f = open('words.txt', 'r')
wordList = []
for line in f:
	if type(line) == str and len(line) > 5:
		wordList.append(str(line[:-2]))

checktrie = make_trie(wordList)


g = open('common.txt', 'r')
wordList2 = []
for line in g:
	if type(line) == str and len(line) > 4:
		wordList2.append(str(line[:-1]))

trie = make_trie(wordList2)


runGame()




