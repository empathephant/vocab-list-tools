# Starting with the third word, every other word has the second half characters replaced with dashes.
# If its an odd numbered character word you keep more letters than dashes.
# If the 3rd word is a single character start with the 4 and do every other one.
# ex: The preliminary da-- suggests th-- his exper----- was anecd-----.

import os
import nltk

def dash_word(word):
    wordLen = len(word)

    if wordLen % 2  == 1 and wordLen != 1:  #odd number of characters
        firstHalf = (wordLen + 1) //2
        secondHalf = (wordLen - 1) // 2
        word = word[:firstHalf]
        dashes = "-" * secondHalf
        word += dashes
        actualWords.add(word) #recognize dashed word as a word still
        return word
    if wordLen % 2  == 0:  #even number of characters
        half = wordLen // 2
        word = word[:half]
        dashes = "-" * half
        word += dashes
        actualWords.add(word) #recognize dashed word as a word still
        return word

def build_sentence(wordBank):
    sentence = ""
    punct = ".:,;\'?"
    nums = "0123456789"
    numWords = len(wordBank) - 1

    for counter, token in enumerate(wordBank):
        # print(str(counter) + ', ' + token)
        if counter != numWords: #if you haven't reached the end of a list
            nextWord = wordBank[counter + 1]

            if token in actualWords or token[0] in punct or token in nums: #if the word needs a space after it
                if nextWord[0] not in punct: #and the next word doesn't demand no space before it
                    token += ' ' #add a space after the word
        sentence += token
    return sentence

def fix_tokens(tokens):
    skipNext = False
    fixedToks = []

    for idx, token in enumerate(tokens):
        if idx == 0 or idx == len(tokens) - 1:
            fixedToks.append(token)
        if idx > 0 and idx < len(tokens) - 1:
            prevTok = tokens[idx - 1]
            nextTok = tokens[idx + 1]

            if token == "’":
                skipNext = True
                contraction ="\'" + nextTok
                fixedToks.append(contraction)

            elif token == "n't":
                fixedToks[-1] = prevTok + 'n'
                contraction = "\'" + 't'
                fixedToks.append(contraction)

            elif skipNext:
                skipNext = False

            else:
                fixedToks.append(token)

    # dashChart.write("original tokens: " + str(tokens) + "\n")
    # dashChart.write("fixed tokens: " + str(fixedToks) + "\n")
    return fixedToks

def find_actual_words(fixedToks):
    punctNum = ":,.!?;\'\"`$1234567890"
    actualWords = set()

    for token in fixedToks:
        if token[0] not in punctNum:
            actualWords.add(token)

    # dashChart.write("set of words: " + str(actualWords) + "\n")
    return actualWords

def find_stubs(fixedToks):
    stubs = set()
    for token in fixedToks:
        if token[0] == "\'":
            stubs.add(token)
    # for stub in stubs:
        # print(stub)
    return stubs

def determine_dashed_words(fixedToks, actualWords, stubs):
    dashedSent = []
    wordIndex = 0
    isWord = False
    nextDash = 3
    lastIdx = len(fixedToks) - 1
    for counter, token in enumerate(fixedToks):
        if counter != lastIdx:
            nextTok = fixedToks[counter + 1]

        if token in actualWords:
            wordIndex += 1
            isWord = True
        else:
            isWord = False;

        if isWord and wordIndex == nextDash:
            if len(token) > 1:
                token = dash_word(token)

                if nextTok[0] == "\'":
                    numLet = (len(nextTok) - 1)
                    # print("numLet: " + str(numLet))
                    numDash = (numLet + 1) // 2
                    # print("numDash: " + str(numDash))
                    dashes = "-" * numDash
                    fixedToks[counter + 1] = "\'" + dashes

                nextDash = wordIndex + 2
            elif nextTok[0] == "\'":
                numLet = (len(nextTok) - 1)
                # print("numLet: " + str(numLet))
                numDash = (numLet + 1) // 2
                # print("numDash: " + str(numDash))
                dashes = "-" * numDash
                fixedToks[counter + 1] = "\'" + dashes
                nextDash = wordIndex + 2
            else:
                nextDash = wordIndex + 1
        dashedSent.append(token)

    # print(dashedSent)
    return dashedSent

dashChart = open("dashedchart.tsv", 'w+')
# toFix = open("testcases2.txt")
toFix = open("toadddashes.txt")
lines = toFix.readlines()

for raw_line in lines:
    tokens = nltk.word_tokenize(raw_line)
    fixedToks = fix_tokens(tokens)
    actualWords = find_actual_words(fixedToks)
    contractStubs = find_stubs(fixedToks)
    dashedSent = determine_dashed_words(fixedToks, actualWords, contractStubs)
    sentence = build_sentence(dashedSent)
    dashChart.write(sentence + "\n")
print("File conversion finished")
