import re
import os

headWordRE = r'([a-z]*\.[vrnj]:)'
synonymRE = r':(\W.*\.)'

fixedChart = open("fixedexcel.tsv", 'w+')

toFix = open("exceltofix.txt")
lines = toFix.readlines()
for line in lines:
    headWord = re.search(headWordRE, line)
    synonym = re.search(synonymRE, line)
    if headWord and synonym:
        fixedChart.write(headWord.group(1) + '\t' + synonym.group(1) + '\n')
print("File conversion finished")
