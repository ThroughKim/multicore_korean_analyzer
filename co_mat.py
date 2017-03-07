import codecs
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

L1 = ["좋", "대하", "많", "없", "듣", "내용", "잘", "이해", "배우", "설명", "감사", "발표", "시험", "알", "도움", "과제", "어렵", "쉽", "토론", "문제", "통하", "공부", "준비", "힘들", "재미있", "가르치", "사람", "방식", "방법", "질문", "다양", "아쉽", "자료", "열심히", "평가", "지식", "흥미", "친절", "안", "아니", "재밌", "참여", "노력", "이야기", "인상깊", "필요", "개선", "이론", "성적", "점수", "유익", "말씀", "부족", "열정적", "열정", "부담", "능력", "의견", "피드백", "소통", "분위기", "관심", "실습", "기준", "즐겁", "진도", "출석", "항상", "선생님",  "교수", "못"]
text_file = codecs.open('test', 'r', encoding='utf8')
L2 = text_file.read().split(',')


res = {}

for s, phrase in enumerate(L2):
    for word1 in phrase.split(" "):
        for word2 in phrase.split(" "):
            if word1 in L1 and word2 in L1:
                output = word1, word2, phrase
                key = (word1, word2)
                res[key] = res.get(key, 0) + 1
fp1 = fm.FontProperties(fname="./NotoSansCJKkr-Regular.otf")
nx.set_fontproperties(fp1)
G = nx.Graph()

for item in res:
    print(item, res[item])
    G.add_edge(item[0], item[1], weight=res[item])

weights= [G[u][v]['weight'] for u,v in G.edges()]
degree = nx.degree(G)

nx.draw(
    G,
    width = weights,
    with_labels = True,
    node_color = 'yellow',
    node_size = [v*100 for v in degree.values()]
)

plt.show()