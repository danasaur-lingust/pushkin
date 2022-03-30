import json
import glob
import os

def gettext(files):
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
            out = json.loads(text)
            with open('result.txt', 'a', encoding='utf-8') as res:
                for x in range(100):
                    output = out['response']['items'][x]['text']
                    if output != '':
                        res.write(output)
                        res.write('\n')

os.chdir(r'C:\Users\User\Desktop\WACOM\Python\2 курс\pushkin')
my_files = glob.glob('*.txt')

gettext(my_files)
