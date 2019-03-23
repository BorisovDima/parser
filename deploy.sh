#!/usr/bin/env bash

python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
exec FLASK_APP=main.py
flask db init 