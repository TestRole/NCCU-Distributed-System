import networkx as nx
import matplotlib.pyplot as plt
import json
from networkx.readwrite import json_graph
from collections import OrderedDict
import math

rl = [(u'USA', u'ISR', 5), (u'GBR', u'USA', 5), (u'USA', u'AFG', 4), (u'ISR', u'USA', 3), (u'USA', u'LBY', 3),
      (u'PSE', u'ISR', 3), (u'USA', u'PAK', 3), (u'USA', u'EGY', 3), (u'USA', u'IRQ', 3), (u'AFR', u'ZAF', 2),
      (u'CHE', u'ARG', 2), (u'FRA', u'ESP', 2), (u'CUB', u'USA', 2), (u'USA', u'GBR', 2), (u'LBN', u'EGY', 2),
      (u'USA', u'MEX', 2), (u'USA', u'RUS', 2), (u'AUS', u'USA', 2), (u'IRN', u'IRQ', 2), (u'RUS', u'USA', 2),
      (u'COL', u'USA', 2), (u'IRQ', u'USA', 2), (u'AUS', u'CHN', 2), (u'BEL', u'USA', 2), (u'USA', u'LKA', 2)]


def create_graph():
    G = nx.Graph()
    for link in rl:
        G.add_edge(link[0], link[1], weight=link[2])
    # print G.nodes(data=True)
    # pos = nx.spring_layout(G)
    '''pos: {u'EGY': array([ 0.33678921,  0.73134312]), u'BEL': array([ 0.00656671,  0.55171227])}'''
    # for name, value in pos.items():
    #     # print name, value
    #     G.node[name]['label'] = str(name)
    #     G.node[name]['x'] = pos[name][0]
    #     G.node[name]['y'] = pos[name][1]

    return G


# G.add_edge('GBR', 'USA', weight=8)
# G.add_edge('USA', 'IRF', weight=6)


def calculate_degree_centrality(G, ct):
    gdict = {}
    if ct == 'degree':
        gdict = nx.degree_centrality(G)
    elif ct == 'closeness':
        gdict == nx.closeness_centrality(G)
    elif ct == 'between':
        gdict == nx.betweenness_centrality(G)
    else:
        print 'not a valid centrality argument!'
        exit()
    od = OrderedDict(sorted(gdict.items(), key=lambda t: t[1], reverse=True)).items()
    for i in od:
        print i[0], i[1]
    return od


def drawing(graph):
    # pos = nx.spring_layout(graph)
    # plt.title(
    #   'Centrality network graph',
    #   y=0.97, fontsize=20, fontweight='bold')
    # nx.draw_networkx_labels(graph, pos, font_size=10, font_family='sans-serif')
    # nx.draw_random(graph)

    '''d = nx.degree(graph)
    print d
    nx.draw(graph, nodelist=d.keys(), node_size=[v * 100 for v in d.values()], with_labels=True)
    '''

    # plt.figure(figsize=(30, 20))
    plt.title(
        'Network Centrality Graph',
        y=0.97, fontsize=20, fontweight='bold')
    cf = plt.gcf()
    ax = cf.gca()
    ax.set_axis_off()

    gmax = max(nx.connected_component_subgraphs(graph), key=len)
    d = nx.degree(gmax)
    b = nx.betweenness_centrality(gmax).items()

    # use a standard spring layout - http://networkx.lanl.gov/reference/drawing.html
    pos = nx.spring_layout(gmax)

    nx.draw_networkx_edges(gmax, pos, nodelist=[v[0] for v in b], node_size=[d[v[0]] * 100 for v in b],
                           with_labels=False, alpha=0.3,
                           node_color=[math.log(1 + v[1] * 1000) for v in b], cmap=plt.cm.Blues,
                           width=[gmax[u][v]['weight'] for u, v in gmax.edges()])
    nx.draw_networkx_nodes(gmax, pos, nodelist=[v[0] for v in b], node_size=[d[v[0]] * 100 for v in b],
                           with_labels=True, alpha=0.9,
                           node_color=[math.log(1 + v[1] * 1000) for v in b], cmap=plt.cm.Blues,
                           width=[gmax[u][v]['weight'] for u, v in gmax.edges()])
    nx.draw_networkx_labels(gmax, pos, nodelist=[v[0] for v in b], node_size=[d[v[0]] * 100 for v in b],
                            with_labels=True,
                            node_color=[math.log(1 + v[1] * 1000) for v in b], cmap=plt.cm.Blues,
                            width=[gmax[u][v]['weight'] for u, v in gmax.edges()])
    plt.show()


def save_graph(G):
    # nx.write_gexf(G, 'test.gexf' )
    with open('a.json', 'w') as outfile1:
        outfile1.write(
            json.dumps(json_graph.node_link_data(G, attrs={'source': 'source', 'target': 'target', 'id': 'id'}),
                       indent=2))


if __name__ == '__main__':
    G = create_graph()
    '''available choice: degree, closeness, between'''
    value_list = calculate_degree_centrality(G, 'degree')

    # assign size = centrality value
    # for i in value_list:
    #     G.node[i[0]]['size'] = i[1]
    #     if i[1] > 0.05:
    #         G.node[i[0]]['color'] = 'blue'

    # count_edge = 1
    # for c1, c2, d in G.edges_iter(data=True):
    #     G.edge[c1][c2]['id'] = 'e' + str(count_edge)
    #     G.edge[c1][c2]['source'] = c1
    #     G.edge[c1][c2]['target'] = c2
    #     d.pop('weight')
    #     count_edge += 1
    #     # print c1, c2, d

    # G = nx.path_graph(4)
    # save_graph(G)
    drawing(G)

