# Importing Flask modules: 
from flask import Blueprint, make_response, render_template, flash, redirect
from flask import current_app as app

# Importing Flask REST API modules:
from flask_restful import Resource, reqparse, Api

# Importing 3rd party packages:
import ast
import json
import datetime
import networkx as nx
import plotly
import plotly.graph_objects as go

# Importing internal packages: 
from .models import MicroServiceLog, Microservice, db
from .forms import MicroserviceCreationForm

# Blueprint Configuration:
microservice_bp = Blueprint(
    "microservice_bp", __name__,
    template_folder = "templates",
    static_folder = "static"
) 

# Creating API:
api = Api(microservice_bp)

# Creating the request parser object for all python logging field:
log_parser = reqparse.RequestParser()
log_parser.add_argument("name")
log_parser.add_argument("msg")
log_parser.add_argument("args")
log_parser.add_argument("levelname")
log_parser.add_argument("created")
log_parser.add_argument("lineno")
log_parser.add_argument("funcName")
log_parser.add_argument("msecs")
log_parser.add_argument("relativeCreated")
log_parser.add_argument("thread")
log_parser.add_argument("threadName")
log_parser.add_argument("processName")
log_parser.add_argument("process")

class MicroServiceLogs(Resource):
    """The REST API functions for handeling python logs sent to the server from 
    velokzz microservices. 

    GET - Display the data based on the query params.
    POST - Ingest Log information.
    PUT - N/A
    DELETE - N/A  
    """
    def get(self):
        """Querying all avalible microservice logs that conform to the url query parameters.

        TODO: Add URL query param support.
        """
        # Querying all logs made from the database:
        logs = MicroServiceLog.query.all()

        # Unpacking the SQLAlchemy objects into seralized JSON:
        reddit_logs = [
            {
                "name":log.name,
                "msg": log.msg,
                "app_name":log.app_name,
                "process_type":log.process_type,
                "timestamp":log.timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
                "status_code": log.status_code,
                "levelname":log.levelname,
                "created":log.created.strftime("%m/%d/%Y, %H:%M:%S"),
                "lineno":log.lineno,
                "funcName":log.funcName,
                "msecs":log.msecs,
                "relativeCreated":log.relativeCreated.strftime("%m/%d/%Y, %H:%M:%S"),
                "thread":log.thread,
                "threadName":log.threadName,
                "processName":log.processName,
                "process":log.process
            }
             for log in logs
             ]
        
        return reddit_logs
    
    def post(self):
        """Handeling POST requests made to the server containing logs.

        The method error checks each post request to ensure that it conforms 
        to a specific structure. If the request body contains the correct params
        the method performs type conversion and unpacks all params to create log
        SQLA objects that are written to the database. 
        """
        
        # Extracting all log params:
        args = log_parser.parse_args()

        if {
            'args', 'created', 'lineno', 'msecs', 'relativeCreated', 
            'thread', 'name', 'msg', 'levelname', 'funcName', 'threadName',
            'processName', 'process'
            } <= set(args):

            # Converting the string tuple to actual tuple and unpacking:
            app_name, process_type, timestamp, status_code = ast.literal_eval(args["args"])

            # Converting the arguments to the correct data types:
            timestamp_obj = datetime.datetime.strptime(timestamp, "%d-%b-%Y (%H:%M:%S.%f)")
            status_code = int(status_code)
            created_obj = datetime.datetime.fromtimestamp(float(args["created"]))
            lineno = int(args["lineno"])
            msecs = float(args["msecs"])
            relativeCreated = datetime.datetime.fromtimestamp(float(args["relativeCreated"]))
            thead = int(args["thread"])
            
            # Creating Log w/ ORM object:
            new_log = MicroServiceLog(
                name = args["name"],
                msg = args["msg"],
                app_name = app_name,
                process_type = process_type,
                timestamp = timestamp_obj,
                status_code = status_code,
                levelname = args["levelname"],
                created = created_obj,
                lineno = lineno,
                funcName = args["funcName"],
                msecs = msecs,
                relativeCreated = relativeCreated,
                thread = thead,
                threadName = args["threadName"],
                processName = args["processName"],
                process = args["process"]
            )

            # Commiting a Log Object to the database:
            db.session.add(new_log)
            db.session.commit() 
            
            return make_response(f"Log {app_name}{process_type}{timestamp_obj} Successfully")

        else:
            raise Warning("Log not Written to the database. Placeholder for error catching.")
            pass

# Registering Microservice Log Routes:
api.add_resource(MicroServiceLogs, "/microservices/api/")

# Non REST API Routes:
@microservice_bp.route("/microservices/", methods=["GET"])
def microservice_log_home():

    # Querying the Microservice objects:
    microservices = Microservice.query.all()

    # Creating the graph plot from all the microservices:
    microservice_G = nx.Graph()
    microservice_G.add_node("Velkozz_REST_API") # Central node for the graph, the velkozz REST API.

    # Adding Microservice objects as nodes to the graph:
    microservice_G.add_nodes_from(microservices)

    for microservice in microservices:
        microservice_G.add_edge(microservice, "Velkozz_REST_API")

    # Generating the positions for each node in the graph:
    pos = nx.spring_layout(microservice_G)

    # formatting the nodes and edges of the graph:
    for n, p in pos.items():
        microservice_G.nodes[n]["pos"] = p

    # Creating the scatter plot for the edges:
    edge_trace = go.Scatter(
        x = [],
        y = [],
        line = dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines"
    )

    # Populating the edge trace with x and y values:
    for edge in microservice_G.edges():
        x0, y0 = microservice_G.nodes[edge[0]]['pos']
        x1, y1 = microservice_G.nodes[edge[1]]['pos']
        edge_trace["x"] += tuple([x0, x1, None]) 
        edge_trace["y"] += tuple([y0, y1, None])
    
    # Creating the scatter plot for graph nodes:
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode="markers",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale='RdBu',
            reversescale=True,
            color=[],
            size=15,
            colorbar=dict(
                thickness=10,
                title='Node Connections',
                xanchor='left',
                titleside='right'),
        line=dict(width=0)))   
    
    # Populating the node scatter trace with x and y values:
    for node in microservice_G.nodes():
        x, y = microservice_G.nodes[node]['pos']
        node_trace["x"] += tuple([x])
        node_trace["y"] += tuple([y])
    
    # Labeling the nodes text and color:
    for node in microservice_G.nodes():
        # Determining if the node is a microservice or the REST API:
        if type(node) == str:
            # Labeling the node:
            node_trace["text"] += tuple([node])
            
            # Setting REST API node color:
            node_trace["marker"]["color"] += tuple(["#FF00FF"]) # This overwrites the scatterplot params w/ config values.

        else:
            # Labeling the node:
            node_trace["text"] += tuple([f"{node.microservice_name} Microservice"])

            # Setting the node color for Microservices:
            node_trace["marker"]['color'] += tuple(["#0000FF"])

    # Creating the total graph figure:
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout = go.Layout(
            title="Test Title",
            titlefont=dict(size=16),
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[dict(
                    text="No. of connections",
                    showarrow=False,
                    xref="paper", yref="paper")],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    # Converting the plotly graph to a JSON object to be passed to the frontend:
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # TODO: Filter the logs sent by microservices.
    # Create line graphs of all of the microservices sent per microservice.

    return render_template("microservice_home.html", microservices=microservices, graphJSON=graphJSON)

# Route for Microservice creation:
@microservice_bp.route("/microservices/add/", methods=["GET", "POST"])
def microservice_creation_form():

    # Creating Microservice creation form:
    form = MicroserviceCreationForm()
    
    # Processing Form info and adding microservice to database:
    if form.validate_on_submit():

        # Creating a Microservice Object:
        new_microservice = Microservice(
            microservice_name=form.microservice_name.data,
            microservice_description=form.microservice_description.data,
            date_added=datetime.datetime.now()
        )

        # Committing a Microservice object to the database:
        db.session.add(new_microservice)
        db.session.commit()

        return redirect("/microservices/")

    return render_template("microservice_creation_form.html", form=form)