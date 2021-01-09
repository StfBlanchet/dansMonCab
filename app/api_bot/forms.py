#!/usr/bin/env python
# coding: utf8

"""
Flask forms
"""

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    entry = TextAreaField('search', validators=[DataRequired()])
    submit = SubmitField('Allons-y !')
