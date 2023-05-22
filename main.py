import parser

import wordModule


if __name__ == '__main__':

    parser = parser.Parser("L6mp3.mdx")
    filename = "cet4medium"
    format = "docx"
    wholeExampleList1 = []
    wholeExampleList2 = []
    wholeExampleListCh = []
    myWords = wordModule.loadWordList(filename + ".txt")
    for word in myWords:
        # print(word)
        wordRes, html = parser.searchWord(word)
        if wordRes is None:
            continue
        res1 = parser.getContentFromHtmlSimplified(html, word)
        res2 = parser.removeTheOriginWord(res1)

        for example in res1['exampleList']:
            wholeExampleList1.append(example)
        for example_ch in res1['exampleList_c']:
            wholeExampleListCh.append(example_ch)
        for example in res2['exampleList']:
            wholeExampleList2.append(example)
    wordModule.writeFile(wholeExampleList1, wholeExampleList2, wholeExampleListCh, filename, format)

