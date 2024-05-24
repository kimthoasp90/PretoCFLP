###############-------------------------------###############
# Run LDA for Documments Clustering with package topicmodels
###############-------------------------------###############

library('NLP')
library('tm')
library('topicmodels')
library("lda")
library("SnowballC")
library("Rmpfr")
#library("RTextTools")


readFile<-function(file_name){
	x <- scan(file_path, what="", sep="\n")
	print(x)
	doc<-""
	for(i in 1:length(x)){
		temp=x[i]
		if (i!=length(x) ){
			temp<-paste0(temp," ",collapse = NULL)
		}
		doc<-paste0(doc,temp,collapse = NULL)
	}
	doc
}


# Register each file in sub_folder
root_folder_path <-"C:/Users/PC/PycharmProjects/LinkPrediction-Pretopology/CrawlAbstractFromsPapers/LDADataset"


# Loop all files in folder and read data from text files
docs<-list()

file.names <- dir(root_folder_path, pattern =".txt")
for (j in 1: length(file.names)){
  file_path<-paste0(root_folder_path,"/",collapse = NULL)
  file_path<-paste0(file_path,file.names[j],collapse = NULL)
  doc <- readFile(file_path)
  print(doc)
  if (doc != ''){
    docs<-c(docs,doc)
  }
}

#-----------------------------------------------------------------------
# set thresthod parametres
k=20 # number of topics
nclusters=20 # number of clusters
iter=5000 # number of iteration for LDA with Gibbs Sampling

# convert docs to the vector format 
docs.vec <- VectorSource(docs)
docs.corpus <- Corpus(docs.vec)
summary(docs.corpus)


#####------------------------------------------------------------####
# Run LDA with package topicmodels
#####-----------------------------------------------------------####

# get the document term matrix using "tm" package
dtm <- DocumentTermMatrix(docs.corpus)

harmonicMean <- function(logLikelihoods, precision=2000L) {
  library("Rmpfr")
  llMed <- median(logLikelihoods)
  as.double(llMed - log(mean(exp(-mpfr(logLikelihoods,
                                       prec = precision) + llMed))))
}

# The log-likelihood values are then determined by first fitting the model using for example
burnin = 1000
iter = 1000
keep = 50


# generate numerous topic models with different numbers of topics
sequ <- seq(10, 100, 10) 
fitted_many <- lapply(sequ, function(k) LDA(dtm, k = k, method = "Gibbs",control = list(burnin = burnin, iter = iter, keep = keep) ))

# extract logliks from each topic
logLiks_many <- lapply(fitted_many, function(L)  L@logLiks[-c(1:(burnin/keep))])

# compute harmonic means
hm_many <- sapply(logLiks_many, function(h) harmonicMean(h))

# compute optimum number of topics
sequ[which.max(hm_many)]
## 6

hm_many

# inspect
plot(sequ, hm_many, type = "l")


plot(sequ, hm_many, type = "l", xlab = "Number of Topics", ylab = "Harmonic mean of Log-Likelihood")

file_optimal_k<-paste0(root_folder_path,'optimal_k.txt',collapse = NULL)
write(sequ[which.max(hm_many)],file=file_optimal_k, ncolumns=1000,append = TRUE, sep = " ")

file_seq_k<-paste0(root_folder_path,'seq_k.txt',collapse = NULL)
write(sequ,file=file_seq_k, ncolumns=1000,append = TRUE, sep = " ")

file_tp_per<-paste0(root_folder_path,'tp_perplexity.txt',collapse = NULL)
write(hm_many,file=file_tp_per, ncolumns=1000,append = TRUE, sep = " ")



