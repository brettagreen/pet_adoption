from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField, TextAreaField
from wtforms.validators import Optional, URL, NumberRange, Length
class AddPetForm(FlaskForm):
    """Form for adding and editing pets."""

    name = StringField("Pet Name")
    species = SelectField("Pet Species", choices=[('dog','dog'), ('cat','cat'), ('porcupine', 'porcupine')])
    photo_url = StringField("Pet photo URL", validators=[URL(), Optional()])
    age = IntegerField("Pet's age", validators=[NumberRange(min=0, max=30), Optional()])
    notes = StringField("Additional notes", validators=[Optional()])

class EditPetForm(FlaskForm):
    """Form for editing an existing pet."""

    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    notes = TextAreaField("Comments", validators=[Optional(), Length(min=10)])
    available = BooleanField("Available?")
    