# import urllib.request

# response = urllib.request.urlopen("https://dl.acm.org/tab_abstract.cfm?id=2389674&type=Article&usebody=tabbody&_cf_containerId=cf_layoutareaabstract&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=629C7C3E84ED6A59A42B07706D5B8611&_cf_rc=0&fbclid=IwAR1sJZBbuGmYheRIU5RK266Iq0rMUEIcCpUbheKKBEF9aYFGVv9aPIp2oBE")
# page_source = response.read()
# print(page_source)

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

import pymysql
import networkx as nx
import csv
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import os

# Connect
db = pymysql.connect(host="localhost",
                     user="root",
                     passwd="****",
                     db="dblpdatabase")
cursor = db.cursor()
cwd = os.getcwd()
FullTextDatasetPath = cwd + "/ExtraTextDataset"
ContinueAbstractTextDatasetPath = cwd + "/AbstractTextDataset"



def crawlabtract():
    papers = {}

    with open("dois.txt", "r")as f:
        lines = f.readlines()

    for line in lines:
        doi=str(line).strip()
        elements = str(doi).strip().split(".")
        paper_id = elements[len(elements) - 1]
        papers.update({paper_id: doi})

    # get abtracts of papers and save into file.
    for paper in papers.keys():
        try:
            print("paperid: ", paper)
            doi = papers[paper]
            # print("doi: ", doi)
            elements = str(doi).strip().split(".")
            id = elements[len(elements) - 1]
            url = "https://dl.acm.org/tab_abstract.cfm?id=" + str(
                id) + "&type=Article&usebody=tabbody&_cf_containerId=cf_layoutareaabstract&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=629C7C3E84ED6A59A42B07706D5B8611&_cf_rc=0&fbclid=IwAR1sJZBbuGmYheRIU5RK266Iq0rMUEIcCpUbheKKBEF9aYFGVv9aPIp2oBE"
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req, timeout=10).read()

            # print(webpage)
            soup = BeautifulSoup(webpage)
            abtractdiv = soup.find("p")
            # print("abtract:  ", abtractdiv.text)
            if abtractdiv==None:
                abtractdiv = soup.find("par")

            # Pre-processing keywords before save into file
            # Firstly, combine keywords into string
            imputstr = abtractdiv.text
            imputstr = imputstr.strip()
            print("inputstr: ", imputstr)

            if "We apologize for this inconvenience" not in imputstr:
                # Convert text to lowercase
                imputstr = imputstr.lower()
                # Remove number in text
                imputstr = re.sub("\d+", " ", imputstr)
                # Remove punctation
                imputstr = imputstr.translate(str.maketrans('', '', string.punctuation))
                # remove white space
                input_str = imputstr.strip()
                # remove stop words
                stop_words = set(stopwords.words('english'))
                tokens = word_tokenize(input_str)
                result = [i for i in tokens if not i in stop_words]
                # stemming:
                stemmer = PorterStemmer()
                outputstr = ""
                for word in result:
                    outputstr += stemmer.stem(word) + " "
                outputstr = outputstr.strip()
                print('outputstr:', outputstr)
                # save output str into file
                filepath = FullTextDatasetPath + "/" + str(paper) + ".txt"
                with open(filepath, "w", encoding='utf-8') as f:
                    f.writelines(outputstr)
            else:
                with open("NewPapersErrorCraw.txt", "a")as f:
                    f.write('{}\n'.format(paper))
        except:
            with open("NewPapersErrorCraw.txt", "a")as f:
                f.write('{}\n'.format(paper))


crawlabtract()
