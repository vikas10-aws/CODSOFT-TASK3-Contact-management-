#!/bin/bash

# Stop any existing Flask application
pkill -f 'flask run'

# Start the Flask application in the background
nohup flask run --host=0.0.0.0 --port=80 > /var/log/flask.log 2>&1 &
