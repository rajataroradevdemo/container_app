# Create our image based on Python 3.8
FROM python:3.8

# Expose ports
EXPOSE 5000

# Tell Python to not generate .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# Turn off buffering
ENV PYTHONUNBUFFERED 1

# Install requirements using pip
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

# Set working directory and addour Flask API files
WORKDIR /app
ADD . /app

#Run gunicorn server for production mode
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

# docker build -t api .

#docker run -p 8000:8000 my-python-image
#
#docker run -e 'MONGODB_HOST=13.201.28.112'  -e 'MONGODB_USERNAME=admin' -e 'MONGODB_PASSWORD=password' -p 5000:5000 -d api
