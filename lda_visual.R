install.packages('tm')
install.packages('stringr')
install.packages('lda')
install.packages('topicmodels')
install.packages('LDAvis')
install.packages('servr')
install.packages('LDAvisData')

install.packages("devtools")
devtools::install_github("cpsievert/LDAvisData")


library(lda)
library(stringr)
library(tm)
library(topicmodels)
library(LDAvis)
library(servr)
library(LDAvisData)


library(MASS)
PimaCV.lda <- lda(type ~ ., data = Pima.tr, CV = TRUE)
tab <- table(Pima.tr$type, PimaCV.lda$class)
conCV1 <- rbind(tab[1, ]/sum(tab[1, ]), tab[2, ]/sum(tab[2, ]))
dimnames(conCV1) <- list(Actual = c("No", "Yes"), "Predicted (cv)" = c("No", "Yes"))
print(round(conCV1, 3))

Pima.lda <- lda(type ~ ., data = Pima.tr)
Pima.hat <- predict(Pima.lda)
tabtrain <- table(Pima.tr$type, Pima.hat$class)


text_data = readLines("total_output", encoding="UTF-8") ## 텍스트 파일의 모든 행 읽어오기
reviews<-text_data
data<-reviews

# read in some stopwords:
library(tm)
stop_words <- stopwords("SMART")

doc.list <- strsplit(reviews, "[[:space:]]+") # 공백을 기준으로 문장 분리
doc.list <- doc.list[lengths(doc.list) >0]    # 빈 줄 삭제

# compute the table of terms:
term.table <- table(unlist(doc.list))
term.table <- sort(term.table, decreasing = TRUE)

# remove terms that are stop words or occur fewer than 3 times:
del <- names(term.table) %in% stop_words | term.table < 5
term.table <- term.table[!del]
vocab <- names(term.table)

# now put the documents into the format required by the lda package:
get.terms <- function(x) {
  index <- match(x, vocab)
  index <- index[!is.na(index)]
  rbind(as.integer(index - 1), as.integer(rep(1, length(index))))
}
documents <- lapply(doc.list, get.terms)

# Compute some statistics related to the data set:
D <- length(documents)  # number of documents (2,000)
W <- length(vocab)  # number of terms in the vocab (14,568)
doc.length <- sapply(documents, function(x) sum(x[2, ]))  # number of tokens per document [312, 288, 170, 436, 291, ...]
N <- sum(doc.length)  # total number of tokens in the data (546,827)
term.frequency <- as.integer(term.table)  # frequencies of terms in the corpus [8939, 5544, 2411, 2410, 2143, ...]

# MCMC and model tuning parameters:
K <- 5
G <- 5000
alpha <- 0.02
eta <- 0.02

# Fit the model:
library(lda)
set.seed(357)
t1 <- Sys.time()
fit <- lda.collapsed.gibbs.sampler(documents = documents, K = K, vocab = vocab,
                                   num.iterations = G, alpha = alpha,
                                   eta = eta, initial = NULL, burnin = 0,
                                   compute.log.likelihood = TRUE)
t2 <- Sys.time()
t2 - t1  # about 24 minutes on laptop

theta <- t(apply(fit$document_sums + alpha, 2, function(x) x/sum(x)))
phi <- t(apply(t(fit$topics) + eta, 2, function(x) x/sum(x)))

MovieReviews <- list(phi = phi,
                     theta = theta,
                     doc.length = doc.length,
                     vocab = vocab,
                     term.frequency = term.frequency)

options(encoding = 'UTF-8') #한글로 결과 보기

# create the JSON object to feed the visualization:
json <- createJSON(phi = MovieReviews$phi,
                   theta = MovieReviews$theta,
                   doc.length = MovieReviews$doc.length,
                   vocab = MovieReviews$vocab,
                   term.frequency = MovieReviews$term.frequency, encoding='UTF-8')

serVis(json, out.dir = 'total_LDA', open.browser = TRUE)