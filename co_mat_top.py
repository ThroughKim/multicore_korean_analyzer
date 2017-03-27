import codecs
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import sys
import time

start_time = time.time()

word_list = [
    '많', '많이', '없', '내용', '이해', '배우', '알', '설명', '감사', '발표', '시험', '중간', '기말', '중간고사', '기말고사',
    '고사', '도움', '과제', '어렵', '부담', '쉽', '토론', '문제', '통하', '소통', '대화', '준비', '재미있', '재밌', '흥미',
    '즐겁', '사람', '학생', '질문', '아쉽', '열심히', '노력', '열정적', '열정', '평가', '지식', '친절', '관심', '배려', '이야기',
    '인상깊', '인상', '성적', '점수', '유익', '능력', '실력', '피드백', '선생님', '교수', '교수님', '수업', '강의', '최고', '완벽',
    '글', '글쓰기', '덕분', '수고', '잘하', '만족', '기억', '사랑', '이름'
]

text_file = codecs.open('testset', 'r', encoding='utf8')
file_sentence_list = text_file.read().split(',')

replace_list = dict(
        많이='많다',
        알다='배우다',
        중간='시험',
        기말='시험',
        중간고사='시험',
        기말고사='시험',
        고사='시험',
        부담='어렵다',
        소통='통하다',
        대화='통하다',
        흥미='재미있다',
        재밌다='재미있다',
        즐겁다='재미있다',
        노력='열심히',
        열정적='열심히',
        열정='열심히',
        관심='친절',
        배려='친절',
        인상='인상깊다',
        점수='성적',
        실력='능력',
        교수='선생님',
        교수님='선생님',
        강의='수업',
        학생='사람',
        알='배우다',
        완벽='최고',
        글쓰기='글',
    )

res = {}
total_lines = len(file_sentence_list)
count = 0

for s, phrase in enumerate(file_sentence_list):
    count+=1
    for word1 in phrase.split(" "):
        word1 = replace_list.get(word1, word1)

        for word2 in phrase.split(" "):
            word2 = replace_list.get(word2, word2)

            if word1 in word_list and word2 in word_list:
                output = word1, word2, phrase
                key = (word1, word2)
                res[key] = res.get(key, 0) + 1

    sys.stdout.write("문장에서 지정 단어 추출 " + str(round(count/total_lines*100,2)) + "% done \r")

# res = {k: v for k, v in res.items() if v > 1}

fp1 = fm.FontProperties(fname="./NotoSansCJKkr-Regular.otf")
nx.set_fontproperties(fp1)
G = nx.Graph()

for item in res:
    G.add_edge(item[0], item[1], weight=res[item])

nx.write_graphml(G, './ graphfile.graphml')

weights= [G[u][v]['weight'] * 0.01 for u,v in G.edges()]
degree = nx.degree(G)

nx.draw_random(
    G,
    with_labels = True,
    font_size = 8,
    node_color = 'yellow',
    edge_color = 'gray',
    width = weights,
    node_size = [v*10 for v in degree.values()]
)
end_time = time.time()

print("걸린 시간" + str(end_time - start_time))

plt.savefig("graph.png", dpi=1000)
#plt.show()
