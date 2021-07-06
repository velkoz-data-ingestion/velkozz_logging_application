# Importing Flask and WTF-Forms methods:
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired 
from wtforms.widgets import TextArea

class MicroserviceCreationForm(FlaskForm):
    # TODO: Create a form for creating a microservice object.
    microservice_name = StringField("Microservice Name", validators=[DataRequired()])
    microservice_description = StringField("Description", widget=TextArea())
    submit = SubmitField("Create Microservice")