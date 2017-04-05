library(tm)
library(wordcloud)

text_data = read.table("total_output", encoding="UTF-8") 
text_data
un_text = table(unlist(text_data))
un_text
wc = sort(un_text, decreasing = T)
pal <- brewer.pal(6, "Dark")
wordcloud(words = names(wc), freq = wc, colors = pal, min.freq = 5, random.order = F, random.color = T, family="AppleGothic", rot.per = 0, scale=c(7,1))
