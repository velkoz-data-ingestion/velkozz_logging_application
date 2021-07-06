# Importing Flask modules: 
from flask import Blueprint, make_response, render_template
from flask import current_app as app

# Creating Velkozz REST API Logger Blueprint:
velkozz_REST_API_bp = Blueprint(
    "velkozz_REST_API_bp", __name__,
    template_folder = "templates",
    static_folder = "static"
) 

# Homepage for the Velkozz REST API Dashboard:
@velkozz_REST_API_bp.route("/velkozz_rest_api/", methods=["GET"])
def velkozz_REST_API_home():
    return render_template("velkozz_REST_API_home.html")
