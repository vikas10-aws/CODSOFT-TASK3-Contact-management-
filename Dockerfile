# Use the official Python base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy application files to the container
COPY app.py requirements.txt /app/
COPY templates /app/templates
COPY static /app/static

# Ensure the CSV files are present (these will be created in the container if missing)
RUN touch /app/contacts.csv /app/users.csv

# Install application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Command to run the application
CMD ["flask", "run"]
