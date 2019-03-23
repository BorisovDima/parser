#!/bin/bash

pip install -r requirements.txt
export FLASK_APP=main.py
flask db init