#! /usr/bin/env python3
# coding: utf-8

"""
dansMonCab chatbot
File that manages the search form.
"""

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    entry = TextAreaField('entry', validators=[DataRequired()])
    submit = SubmitField('Je vous écoute !')
