install.packages('wordcloud')
library(wordcloud)                  # 워드클라우드 패키지 설치 및 로드

text_data = read.table("low_output", encoding="UTF-8")  # cloud_word_extractor.py의 결과 파일 로드
un_text = table(unlist(text_data))      # 파일의 텍스트를 단어와 빈도수로 이루어진 테이블로 변환
wc = sort(un_text, decreasing = T)      # 내림차순 정렬
pal <- brewer.pal(6, "Dark2")           # 워드클라우드 텍스트 컬러 지정
# 워드클라우드 생성(5회 미만 생략)
wordcloud(words = names(wc), freq = wc, colors = pal, min.freq = 5, random.order = F, random.color = T, family="AppleGothic", rot.per = 0, scale=c(7,1))
