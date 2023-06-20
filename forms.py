from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class InsertForm(FlaskForm):
    deptid = StringField('Department ID', validators=[DataRequired(), Length(min=2, max=5)])
    deptname = StringField ('Department Name', validators=[DataRequired(), Length(min=2, max=100)])
    city = StringField ('City', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Insert Record')

class UpdateForm(FlaskForm):
    deptid = StringField('Department ID', validators=[DataRequired(), Length(min=2, max=5)])
    deptname = StringField ('Department Name', validators=[DataRequired(), Length(min=2, max=100)])
    city = StringField ('City', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Update Record')