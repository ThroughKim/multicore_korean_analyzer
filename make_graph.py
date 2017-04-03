import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import time

G = nx.read_graphml('./top.graphml')
fp1 = fm.FontProperties(fname="./NotoSansCJKkr-Regular.otf", size=8)
nx.set_fontproperties(fp1)

weights= [G[u][v]['weight'] * 0.002 for u,v in G.edges()]
degree = nx.degree(G)

node_size_by_freq = []
for n in G.nodes():
    node_freq = G[n][n]['weight']
    node_size_by_freq.append(node_freq/3)

nx.draw_random(
    G,
    with_labels = True,
    node_color = 'yellow',
    edge_color = 'gray',
    width = weights,
    node_size = node_size_by_freq
)
end_time = time.time()

plt.show()
