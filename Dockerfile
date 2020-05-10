FROM python:3.7-slim

# set workdir
WORKDIR /app

# Install any necessary dependencies
ADD requirements.txt /app
RUN pip install -r requirements.txt

# Open port 80 for serving the webpage
EXPOSE 8080

# add app
ADD . /app

# Run app.py when the container launches
CMD gunicorn 'app:get_app()' -b 0.0.0.0:8080 --access-logfile '-'
