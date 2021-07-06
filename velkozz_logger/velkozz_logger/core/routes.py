# Importing Flask modules: 
from flask import Blueprint, render_template
from flask import current_app as app

# Blueprint Configuration: 
core_bp = Blueprint(
    "core_bp", __name__,
    template_folder = "templates",
    static_folder = "static"
)

# Test Initial Route:
@core_bp.route("/", methods=["GET"])
def home():
    return render_template("home.html")