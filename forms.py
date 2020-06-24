from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, TextAreaField, SubmitField, MultipleFileField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, NumberRange
from wtforms import Form, FormField
from wtforms.fields import FieldList


class BaseForm(FlaskForm):
    numberLumpSum = IntegerField('Number of Lump Sums', default=0, validators=[NumberRange(min=0,max=20)])
    addLumpSum = SubmitField('Add Lump Sum')


class LumpForm(Form):
    lumpSumAmount = IntegerField('Amount of Lump Sum', validators=[InputRequired(),NumberRange(min=100)])
    lumpSumDate = DateField('Date of Lump Sum', format='%Y-%m-%d', validators=[InputRequired()])


class ReqForm(FlaskForm):
    fundCode = IntegerField('Fund Code', validators=[InputRequired()])
    startDate = DateField('SIP Start Date', format='%Y-%m-%d', validators=[InputRequired()])
    endDate = DateField('SIP End Date', format='%Y-%m-%d', validators=[InputRequired()])
    sipAmount = IntegerField('SIP Amount', validators=[InputRequired(),NumberRange(min=100)])

    lumpSums = FieldList(FormField(LumpForm), min_entries=0)
    numberLumpSum = IntegerField('Number of Lump Sums', default=0, validators=[NumberRange(min=0,max=20)])
    submit = SubmitField('Calculate')


















