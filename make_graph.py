# 생성된 graphml 파일을 이용해 실제 그래프를 그림
# 문장을 분석해 graph타입으로 만드는 과정의 시간이 오래 걸리며,
# 그래프를 적절하게 표현하기 위해 변수를 자주 변경해야 하기 때문에 스크립트를 분리

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import time

G = nx.read_graphml('./top.graphml')                    # graphml 파일을 불러
weight_adj = 0.003                                      # 그래프의 edge 두께 조정값
node_size_adj = 4                                       # 그래프의 node 크기 조정값

fp1 = fm.FontProperties(                                # 한글 출력 가능한 폰트 지정과, 폰트 사이즈 지정
    fname="./NotoSansCJKkr-Regular.otf",
    size=8
)
nx.set_fontproperties(fp1)

weights= [                                              # 그래프의 각 요소간 edge 생성 및 설정한 조정값 반영
    G[u][v]['weight'] * weight_adj for u,v in G.edges()
]

node_size_by_freq = []                                  # 단어별 node 크기를 저장할 리스트 생성
for n in G.nodes():                                     # 개별 node에 대해 작업
    node_freq = G[n][n]['weight']                       # node의 weight(빈도)값 추출
    node_size_by_freq.append(node_freq/node_size_adj)   # 미리 설정한 조정값을 반영한 뒤 리스트에 저장

nx.draw_random(                                         # random 혹은 circular 타입의 그래프를 그림
    G,
    with_labels = True,
    node_color = 'yellow',
    edge_color = 'gray',
    width = weights,
    node_size = node_size_by_freq
)
end_time = time.time()

plt.show()                                              # python plt 라이브러리를 이용해 완성된 그래프를 출력
                                                        # 배치가 랜덤이기 때문에 여러번 반복 실행하여 적절한 그래프를 선택 후 저장