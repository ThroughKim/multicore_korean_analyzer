import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import time

G = nx.read_graphml('./top.graphml')
fp1 = fm.FontProperties(fname="./NotoSansCJKkr-Regular.otf", size=8)
nx.set_fontproperties(fp1)

weights= [G[u][v]['weight'] * 0.003 for u,v in G.edges()]
degree = nx.degree(G)

nx.draw_random(
    G,
    with_labels = True,
    node_color = 'yellow',
    edge_color = 'gray',
    width = weights,
    node_size = [v*v*1.5 for v in degree.values()]
)
end_time = time.time()

# plt.savefig("top_graph.png", dpi=500)
plt.show()
