# 필요 패키지 설치 및 로드
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

# lda_sentense_extractor.py의 결과 파일 로드
text_data = readLines("test_lda_wordset", encoding="UTF-8")
doc.list <- strsplit(text_data, "[[:space:]]+") # 공백을 기준으로 문장 분리
doc.list <- doc.list[lengths(doc.list) >0]    # 빈 줄 삭제

# 빈도수 계산하여 테이블로 출력
term.table <- table(unlist(doc.list))
term.table <- sort(term.table, decreasing = TRUE)

# 예외 단어 및 5회 미만 출현 단어 삭제
stop_words <- stopwords("SMART")
del <- names(term.table) %in% stop_words | term.table < 5
term.table <- term.table[!del]
vocab <- names(term.table)

# LDA 패키지에 적합한 형태로 변형
get.terms <- function(x) {
  index <- match(x, vocab)
  index <- index[!is.na(index)]
  rbind(as.integer(index - 1), as.integer(rep(1, length(index))))
}
documents <- lapply(doc.list, get.terms)

# 데이터 셋에 관련된 값 계산
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
fit <- lda.collapsed.gibbs.sampler(documents = documents, K = K, vocab = vocab,
                                   num.iterations = G, alpha = alpha,
                                   eta = eta, initial = NULL, burnin = 0,
                                   compute.log.likelihood = TRUE)

theta <- t(apply(fit$document_sums + alpha, 2, function(x) x/sum(x)))
phi <- t(apply(t(fit$topics) + eta, 2, function(x) x/sum(x)))

Text_words <- list(phi = phi,
                     theta = theta,
                     doc.length = doc.length,
                     vocab = vocab,
                     term.frequency = term.frequency)

options(encoding = 'UTF-8') #한글로 결과 보기

# JSON 타입으로 저장 및 시각화
json <- createJSON(phi = Text_words$phi,
                   theta = Text_words$theta,
                   doc.length = Text_words$doc.length,
                   vocab = Text_words$vocab,
                   term.frequency = Text_words$term.frequency, encoding='UTF-8')

# 시각화 된 파일 지정 폴더로 출력
serVis(json, out.dir = 'test_LDA', open.browser = TRUE)