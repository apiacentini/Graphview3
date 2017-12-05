from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import networkx as nx
from hashlib import sha1
from datetime import datetime
import os


UPLOAD_FOLDER = os.path.join('static', 'resources') #'./static/resources/upload/'  # Save path from server point of view
SIMPLE_UPLOAD_FOLDER = 'resources/'  # Save path from JS point of view
ALLOWED_EXTENSIONS = {'csv'}  # Allowed extensions for uploaded file
UPLOAD_FIELD = 'graph'  # Var name for upload.html file

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'Zupasecret'


@app.route('/', methods=['POST', 'GET'])
def index():
    """
    Main activities:
        If the endpoint is called with a 'GET' method the server will redirect the user to an html page giving the user
        the ability to upload a '.csv' or '.txt' file.
        Otherwise if is called with a 'POST' method the user will visualize the rendered graph based on the previously
        uploaded file and the triadic census of the graph.
    """
    if request.method == 'POST':
        if UPLOAD_FIELD not in request.files:  # Check if the file is in the request
            flash('No file part')
            return redirect(request.url)  # If error, redirect user.
        file = request.files[UPLOAD_FIELD]
        if file.filename == '':  # Check if the filename is valid
            flash('No selected file')
            return redirect(request.url)  # If not, redirect user.
        if file and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:  # Check if the file has a valid extension
            dt = datetime.now()
            filename = secure_filename(file.filename)  # Get filename
            filename = "{}-{}".format(dt.microsecond, filename)  # Join filename and timestamp
            h = sha1(filename.encode())  # Get sha1 of the previously computed string
            filename = h.hexdigest() + ".csv"  # Get the digest
            full_path = os.path.join(UPLOAD_FOLDER, filename)  # Full filename server side
            full_path_js = os.path.join(SIMPLE_UPLOAD_FOLDER, filename)  #  Full filename JS side
            file.save(full_path)  # Save file
            tc = get_tc(full_path)  # Compute TC
            return render_template("index.html", tc=tc, name=full_path_js)  # Return the HTML page
    return render_template("upload.html")  # If request.method == GET


@app.errorhandler(404)
def hand404(e):
    return "<h2>Not found</h2>"

@app.errorhandler(500)
def hand500(e):
    return "<h2>Not found</h2>"


def get_tc(csv_name):
    """
    The method computes the triad census on the uploaded file.

    :param csv_name: CSV filename
    :type csv_name: String
    :return: list containing dicts having keys: tn and count representing triad name and triad count
    :rtype: list
    """
    G = nx.MultiDiGraph()  # create a Supergeil Graph
    with open(csv_name) as csv_file:  # Open the file
        _ = csv_file.readline()  # Ignore first line (Header)
        for line in csv_file.readlines():  # Iterates on the whole file
            line = line.rstrip()  # Ignore the final /n
            nodo1, nodo2 = line.split(",")  # Split the two values and put them in two variables
            if not G.has_node(nodo1):  # If the first node is not already in the graph will add it
                G.add_node(nodo1)
            if not G.has_node(nodo2):  # If the second node is not already in the graph will add it
                G.add_node(nodo2)
            G.add_edge(nodo1, nodo2)  # Create the edge based on the two nodes
    final_triad = nx.triadic_census(G)
    return sorted([{'tn': k, 'count': v} for k, v in final_triad.items()], key=lambda k: k['tn'])



if __name__ == '__main__':
    app.run()
