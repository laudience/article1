import json
from utilitaires import import_data
import igraph as ig
import plotly
import plotly.graph_objs as go

def clean_data(writing):
    deputy_dict = import_data('data.csv')
    with open('relations 18-08-16.json', 'r') as infile:
        relations_data = json.load(infile)
    clean_dict=dict()
    for deputy1 in relations_data:
        for deputy2 in relations_data[deputy1]:
            if relations_data[deputy1][deputy2]['retweets'] != 0:
                if relations_data[deputy1][deputy2]['mentions'] != 0:
                    clean_dict[deputy1]=dict()
                    clean_dict[deputy1][deputy2]=relations_data[deputy1][deputy2]

    if writing is True:
        with open('relations_clean.json', 'w') as outfile:
            json.dump(clean_dict, outfile)
        print("data imported, json writed")


def network_plot(link_type):
    deputy_dict=import_data('data.csv')
    with open('relations.json', 'r') as infile:
        relations_data = json.load(infile)
    nodes = [deputy for deputy in deputy_dict]
    Edges = []
    for deputy1 in nodes:
        for deputy2 in relations_data[deputy1]:
            if relations_data[deputy1][deputy2][link_type] != 0:
                Edges.append((nodes.index(deputy1), nodes.index(deputy2)))
    G=ig.Graph(Edges, directed=False)
    N=len(nodes)
    labels = [deputy_dict[nodes[i]] for i in range(N)]
    layt = G.layout('kk',dim=3)
    Xn = [layt[k][0] for k in range(N)]
    Yn = [layt[k][1] for k in range(N)]
    Zn = [layt[k][2] for k in range(N)]
    Xe = []
    Ye = []
    Ze = []
    for e in Edges:
        Xe += [layt[e[0]][0], layt[e[1]][0], None]
        Ye += [layt[e[0]][1], layt[e[1]][1], None]
        Ze += [layt[e[0]][2], layt[e[1]][2], None]

    trace1 = go.Scatter3d(x=Xe,
                       y=Ye,
                       z=Ze,
                       mode='lines',
                       line=go.Line(color='rgb(125,125,125)', width=1),
                       hoverinfo='none'
                       )
    trace2 = go.Scatter3d(x=Xn,
                       y=Yn,
                       z=Zn,
                       mode='markers',
                       name='deputies',
                       marker=go.Marker(symbol='dot',
                                     size=6,
                                     colorscale='Viridis',
                                     line=go.Line(color='rgb(50,50,50)', width=0.5)
                                     ),
                       text=labels,
                       hoverinfo='text'
                       )
    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title='')
    layout = go.Layout(title="Test",
                        width=1000,
                        height=1000,
                        showlegend=False,
                        hovermode='closest')
    data = go.Data([trace1, trace2])
    fig = go.Figure(data=data, layout=layout)

    plotly.offline.plot(fig, filename=''.join([link_type,'-','relation.html']))


def main():
    #network_plot(link_type='mentions')
    clean_data(writing=True)

if __name__ == '__main__':
    main()
