FROM python:3.5-slim

# set workdir
WORKDIR /app

# Install any necessary dependencies
ADD requirements.txt /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install make

# Open port 80 for serving the webpage
EXPOSE 8080

# add app
ADD . /app

# Run app.py when the container launches
CMD make
