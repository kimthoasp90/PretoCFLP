from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os, io, math, json


def Hellinger(p, q):
    list_of_squares = []
    for p_i, q_i in zip(p, q):
        # caluclate the square of the difference of ith distr elements
        s = (math.sqrt(p_i) - math.sqrt(q_i)) ** 2

        # append
        list_of_squares.append(s)

    # calculate sum of squares
    sosq = sum(list_of_squares)

    return math.sqrt(sosq) / math.sqrt(2)

cwd = os.getcwd()
dataset_dir = cwd + "/LDADataset"
corpus = []
index_author_dict={}

files=os.listdir(dataset_dir)
for file in files:
    with io.open(dataset_dir + '/' + file, errors='ignore', encoding='utf-8') as fid:
        doc=fid.read().strip()
        if doc!="":
            index=len(corpus)
            corpus.append(doc)
            author = str(file).replace(".txt", "")
            index_author_dict.update({index: author})

# Initialize an instance of tf-idf Vectorizer
tfidf_vectorizer = TfidfVectorizer()
# Generate the tf-idf vectors for the corpus
tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
print(tfidf_matrix)
# compute and print the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


def tfidf_sim(author1_id, author2_id):
    index_author1 = ""
    index_author2 = ""
    for index, author in index_author_dict.items():
        if author == author1_id:
            index_author1 = index
        if author == author2_id:
            index_author2 = index

    try:
        return cosine_sim[index_author1, index_author2]
    except:
        return 0

def extract_content_features():
    with open("Dataset[1995, 2010]_[2011, 2015].txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        elements = line.strip().split(",")
        author1_id = elements[0]
        author2_id = elements[1]
        label = elements[2]
        s_tfidf = tfidf_sim(author1_id, author2_id)

        # similar about topic distribution
        filename = "Author_Topics_Distribution_LDA.json"
        with open(filename) as data_file:
            LDAdata = json.load(data_file)
        source_topicdistribution = LDAdata[author1_id]
        target_topicdistribution = LDAdata[author2_id]
        d = Hellinger(source_topicdistribution, target_topicdistribution)
        homo = 1 - d

        with open("Content_features.txt", "a") as fw:
            fw.write('{}, {}, {}, {}, {}\n'.format(author1_id, author2_id, s_tfidf, homo, label))
            fw.close()

extract_content_features()