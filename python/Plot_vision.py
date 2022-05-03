import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import pandas as pd
from mpld3 import plugins
from utils import domain_from
from HypeParameters import css, data_name


def beutiful_plot(crawlers, node_size=100, edge_width=2, circle_size=40, figsize=(20, 40)):
    crawlers = crawlers if isinstance(crawlers, list) else [crawlers]
    fig, ax = plt.subplots(len(crawlers), 2, figsize=figsize)
    TYPE = ['URL', 'Domain']
    for k, crw in enumerate(crawlers):
        text = [f'{crw.main_url[:60]}...' if len(crw.main_url) >= 50 else crw.main_url, domain_from(crw.main_url)]
        Graphs = [crw.knowlage_graph, crw.domain_graph]

        attrs = [{'node_color': nx.get_node_attributes(G, 'color').values(),
                  'edge_color': nx.get_edge_attributes(G, 'color').values(),
                  'arrows': True, 'arrowstyle': '<->'} for G in Graphs]

        handles = [[mpatches.Patch(label=k, color=v) for k, v in lgd.items()] for lgd in
                   [crw.legends, crw.legends_domain]]

        for i, Gra in enumerate(Graphs):
            Ax = ax[i] if len(crawlers) == 1 else ax[k, i]
            nx.draw_kamada_kawai(Gra, **attrs[i], node_size=node_size, width=edge_width, ax=Ax, with_labels=False)
            Ax.set_title(
                f'crawl of {TYPE[i]} : {text[i]} \n,    '
                f'{data_name} found : {len(crw.datas)}')
            Ax.grid(alpha=0.25)
            Ax.legend(handles=handles[i], fontsize=14)
            Ax.axis('on')

            positions = nx.kamada_kawai_layout(Gra)

            points_x = []
            points_y = []
            dict_data = {'data': []}
            for node, (x, y) in positions.items():
                dict_data['data'].append(node)
                points_x.append(x)
                points_y.append(y)

            df = pd.DataFrame(dict_data, columns=['data'])

            labels = []
            for i in range(len(df)):
                label = df.iloc[[i], :].T
                label.columns = [f'link {i + 1}']
                labels.append(str(label.to_html()))

            points = Ax.plot(points_x, points_y, 'o', color='b', mec='k', ms=circle_size, mew=1, alpha=0.1, mfc='none')
            tooltip = plugins.PointHTMLTooltip(points[0], labels, voffset=10, hoffset=10, css=css)
            plugins.connect(fig, tooltip)
    return fig