import xml.sax
import re
import sys
import os
import spacy
# from nltk.stem.porter import *
import en_core_web_sm
# from helper import *
import math
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer

total_word_counter = 0  # to write in invertedindex_stat.txt
stemmer = SnowballStemmer("english")
# stemmer = PorterStemmer()
# nlp = spacy.load('en')
nlp = en_core_web_sm.load()
stop_words = spacy.lang.en.stop_words.STOP_WORDS
term_count=1
termid={}
docid_pageid={}
write_doc_count=0
temp_dict={}
global_dict={}
local_doc_count=0
not_words=["meta","the","inter","brief","belong","text","local","redirect","left"]
# ------------RegularExpressions---------------------
# link
regExp1 = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.DOTALL)
#
regExp2 = re.compile(r'{\|(.*?)\|}', re.DOTALL)
# citation
regExp3 = re.compile(r'{{v?cite(.*?)}}', re.DOTALL)
# Removing the symbols
regExp4 = re.compile(r'[-.,:;_?()"/\']', re.DOTALL)
# Simple Cleaning
regExp5 = re.compile(r'\[\[file:(.*?)\]\]', re.DOTALL)
regExp6 = re.compile(r'[\'~` \n\"_!=@#$%-^*+{\[}\]\|\\<>/?]', re.DOTALL)
# To find words in category field
catRegExp = r'\[\[category:(.*?)\]\]'
# To find words in infobox field
infoRegExp = r'{{infobox(.*?)}}'
# To find words in references field
refRegExp = r'== ?references ?==(.*?)=='
regExp7 = re.compile(infoRegExp, re.DOTALL)
regExp8 = re.compile(refRegExp, re.DOTALL)
regExp9 = re.compile(r'{{(.*?)}}', re.DOTALL)
regExp10 = re.compile(r'<(.*?)>', re.DOTALL)

def remove_new_line(text):
    text = text.replace('\'', '')
    text = text.strip()
    return text.replace('\n', ' ')


def isValid(word):
    if word == "" or word in stop_words or len(word) < 3 or word in not_words:
        return False
    else:
        return True


def clean(tl):
    tl = ' '.join(tl)
    tl = regExp4.sub(' ', tl)
    tl = regExp5.sub(' ', tl)
    tl = regExp6.sub(' ', tl)
    tl = tl.replace('[', ' ')
    tl = tl.replace(']', ' ')
    tl = tl.split()
    return tl


def process_references(b1):
    global term_count, termid, temp_dict
    refers = []
    refers = re.findall(refRegExp, b1, flags=re.DOTALL)
    tl = clean(refers)
    not_refers = ['reflist', 'ref', 'em', 'colwidth']
    t_dict = {}
    for t in tl:
        w = stemmer.stem(t)
        w = remove_new_line(w)
        if isValid(w) and w not in not_refers:
            if w not in termid:
                termid[w] = term_count
                term_count += 1

            if w in temp_dict:
                temp_dict[w][6] += 1
            else:
                temp_dict[w] = [0] * 8
                temp_dict[w][6] += 1
            temp_dict[w][7] += 1
            temp_dict[w][0] = local_doc_count


def process_links(b1, cat_i):
    global term_count, termid, temp_dict
    links = []
    t_dict = {}
    link_i = -1
    try:
        link_i = b1.index('=external links=') + 20
    except:
        pass
    if link_i != -1:
        links = b1[link_i:cat_i]
        links = re.findall(r'\[(.*?)\]', links, flags=re.MULTILINE)
        tl = links
        tl = clean(tl)
        for t in tl:
            w = stemmer.stem(t)
            w = remove_new_line(w)
            if isValid(w):
                if w not in termid:
                    termid[w] = term_count
                    term_count += 1

                if w in temp_dict:
                    temp_dict[w][5] += 1
                else:
                    temp_dict[w] = [0] * 8
                    temp_dict[w][5] += 1
                temp_dict[w][7] += 1
                temp_dict[w][0] = local_doc_count
        process_references(b1)


def process_category(b1):
    global term_count, termid, temp_dict
    cat1 = re.findall(catRegExp, b1, flags=re.MULTILINE)  # returns a list of strings
    for i in cat1:
        tl = i.split()
        tl = clean(tl)
        for t in tl:
            w = stemmer.stem(t)
            w = remove_new_line(w)
            if isValid(w):
                if w not in termid:
                    termid[w] = term_count
                    term_count += 1

                if w in temp_dict:
                    temp_dict[w][4] += 1
                else:
                    temp_dict[w] =[0] * 8
                    temp_dict[w][4] += 1
                temp_dict[w][7] += 1
                temp_dict[w][0] = local_doc_count

    cat_i = -1
    try:
        cat_i = b1.index('[[category:') + 20
    except:
        pass

    if (cat_i == -1):
        cat_i = len(b1)

    process_links(b1, cat_i)


def process_infobox(b1):
    global term_count, termid, temp_dict
    ib1 = re.findall(infoRegExp, b1, re.DOTALL)  # returns a list of strings

    for i in ib1:
        tl = re.findall(r'=(.*?)\|', i, re.DOTALL)
        tl = clean(tl)
        for t in tl:
            w = stemmer.stem(t)
            w = remove_new_line(w)
            if isValid(w):
                if w not in termid:
                    termid[w] = term_count
                    term_count += 1

                if w in temp_dict:
                    temp_dict[w][2] += 1
                else:
                    temp_dict[w] = [0] * 8
                    temp_dict[w][2] += 1
                temp_dict[w][7] += 1
                temp_dict[w][0] = local_doc_count


def body_process(b1):
    global term_count, termid, temp_dict
    b1 = b1.lower()
    b1 = regExp1.sub(' ', b1)
    b1 = regExp2.sub(' ', b1)
    b1 = regExp3.sub(' ', b1)
    b1 = regExp10.sub(' ', b1)
    b1 = remove_new_line(b1)

    process_infobox(b1)
    process_category(b1)

    b1= regExp4.sub(' ', b1)
    b1= regExp5.sub(' ', b1)
    b1= regExp6.sub(' ', b1)
    b1= regExp7.sub(' ', b1)

    b1 = b1.split()
    t_dict = {}
    for b in b1:
        w = stemmer.stem(b)
        if isValid(w):
            if w not in termid:
                termid[w] = term_count
                term_count += 1

            if w in temp_dict:
                temp_dict[w][3] += 1
            else:
                temp_dict[w] = [0] * 8
                temp_dict[w][3] += 1
            temp_dict[w][7] += 1
            temp_dict[w][0] = local_doc_count


def title_process(l1):
    global term_count,termid,temp_dict
    l1 = l1.lower()
    l1 = regExp4.sub(' ', l1)
    l1 = regExp5.sub(' ', l1)
    l1 = regExp6.sub(' ', l1)
    l1 = regExp10.sub(' ', l1)
    l1 = remove_new_line(l1)
    l1 = l1.split()
    t_dict = {}
    for l in l1:
        w = stemmer.stem(l)
        if isValid(w):
            if w not in termid:
                termid[w]=term_count
                term_count+=1

            if w in temp_dict:
                temp_dict[w][1]+=1
            else:
                temp_dict[w]=[0]*8
                temp_dict[w][1]+=1
            temp_dict[w][7] += 1
            temp_dict[w][0]=local_doc_count

def Dismantle(obj):
    title_process(obj.title)
    body_process(obj.body)


def write_temp_doc_1000():
    global write_doc_count,local_doc_count,temp_dict,global_dict
    if not os.path.exists("TempIndex/"):
        os.makedirs("TempIndex/")
    fo=open("TempIndex/"+str(write_doc_count)+".txt","w")
    for i in global_dict.keys():
        str1=str(termid[i])
        for j in global_dict[i]:
            str1=str1+":"
            for k in j:
                str1=str1+str(k)+","
            str1=str1.rstrip(",")
        str1=str1+"\n"
        print(global_dict[i])
        print(i,str1)
        fo.write(str1)
        str1=""
    global_dict.clear()
    write_doc_count+=1


class wikiHandler(xml.sax.ContentHandler):
    global docid_pageid,temp_dict,local_doc_count
    def __init__(self):
        self.current_tag = ""
        self.body = ""
        self.title = ""
        self.id=""

    def startElement(self, tag, attributes):
        self.current_tag = tag

    def endElement(self, tag):
        global docid_pageid, temp_dict, local_doc_count,global_dict
        if (tag == "page"):               #to name the text file like that
            for i in temp_dict.keys():
                temp_dict[i][0]=local_doc_count
            for i in temp_dict.keys():
                if i in global_dict.keys():
                    # print(i,global_dict[i])
                    global_dict[i].append(temp_dict[i])
                else:
                    global_dict[i]=[temp_dict[i]]
            temp_dict.clear()
            x=write_doc_count*1000+local_doc_count
            docid_pageid[x]=[self.id,self.title]
            Dismantle(self)
            if(local_doc_count==1000):
                local_doc_count=0
                write_temp_doc_1000()
                temp_dict.clear()
            self.title=""
            self.body=""
            local_doc_count += 1


    def characters(self, content):
        if self.current_tag == "title":
            self.title += content
        if self.current_tag == "text":
            self.body += content
        if self.current_tag == "id":
            self.id += content

# -------------main----------
path="SampleDump.xml"

# Parsing Part
parser = xml.sax.make_parser()
handler = wikiHandler()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)
parser.setContentHandler(handler)

for directory, subdirlist, filelist in os.walk('/Data'):
    print(filelist)


