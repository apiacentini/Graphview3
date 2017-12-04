from flask import Flask, render_template
import networkx as nx
from os import path

app = Flask(__name__, static_url_path='')


@app.route('/')
def hello_world():
    tc = get_tc('xxxx')
    return render_template("index.html", tc=tc, name='csv.csv')


def get_tc(csv_name):
    G = nx.DiGraph()
    G.add_node('1')
    G.add_node('2')
    G.add_node('3')
    G.add_node('4')
    G.add_edge('1','2')
    G.add_edge('1','3')
    G.add_edge('1','4')
    G.add_edge('3','4')
    G.add_edge('2','3')
    G.add_edge('2','4')
    xxx = nx.triadic_census(G)
    print(xxx)
    return [{'k': k, 'v': v} for k, v in xxx.items()]



if __name__ == '__main__':
    app.run()
