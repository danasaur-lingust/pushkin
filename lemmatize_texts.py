from pymystem3 import Mystem
import io

m = Mystem()
with io.open('result.txt', 'r', encoding = 'utf8') as f:
    tekst = f.read()
lemmas = m.lemmatize(tekst)
ana = m.analyze(tekst)

lexlist = []
wordlist = []
for word in ana:
    if 'analysis' in word:
        lex = word['analysis'][0]['lex']
        token = word['text']
        lexlist.append(lex)
        wordlist.append(token)
with io.open('lexlist.txt', 'w', encoding = 'utf-8') as f:
    for word in lexlist:
        f.write(word + "\n")
with io.open('wordlist.txt', 'w', encoding = 'utf-  8') as f:
    for word in wordlist:
        f.write(word + "\n")
