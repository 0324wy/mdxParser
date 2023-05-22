#  Copyright (C) 2023 Baidu, Inc. All Rights Reserved.
import random

def loadWordList(fileName):
    myWord = []
    with open(fileName) as f:
        line = f.readline()
        while line:
            line = line.replace("\n", "")
            if line.isalpha():
                myWord.append(line)
            # print(len(myWord))
            line = f.readline()
        f.close()
    return myWord

def writeFile(wholeExampleList1, wholeExampleList2, wholeExampleListCh, fileName, format):
    randnum = random.randint(0,100)

    random.seed(randnum)
    random.shuffle(wholeExampleList1)
    random.seed(randnum)
    random.shuffle(wholeExampleList2)
    random.seed(randnum)
    random.shuffle(wholeExampleListCh)
    print(wholeExampleList1[:3])
    print(wholeExampleList2[:3])
    print(wholeExampleListCh[:3])

    f1 = open(fileName + "-1." + format, "w")
    for i in range(len(wholeExampleList1)):
        content = str(i) + '. ' + wholeExampleList1[i] + "\n"
        f1.write(content)
    f1.close()

    f2 = open(fileName + "-2." + format, "w")
    for i in range(len(wholeExampleList2)):
        content = str(i) + '. ' + wholeExampleList2[i] + "\n"
        f2.write(content)
    f1.close()

    f3 = open(fileName + "-ch." + format, "w")
    for i in range(len(wholeExampleListCh)):
        content = str(i) + '. ' + wholeExampleListCh[i] + "\n"
        f3.write(content)
    f3.close()

