# Importing Flask modules: 
from flask import Blueprint, make_response
from flask import current_app as app

# Importing Flask REST API modules:
from flask_restful import Resource, reqparse, Api

# Importing 3rd party packages:
import ast
import json
import datetime

# Importing internal packages: 
from .models import MicroServiceLog, db

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
    return "Microservice Log Home Page"