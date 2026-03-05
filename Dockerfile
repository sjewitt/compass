FROM python:3.10-alpine

# location in the container
WORKDIR /code

# copy the reqs to working dir:
COPY requirements.txt requirements.txt

# put the reqs in the container:
# RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install -r requirements.txt
RUN pip install --no-cache-dir debugpy

EXPOSE 8080

# copy the application code to working dir in container
COPY . .

# CMD ["python", "compass.py", "--port", "8080"]
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678",  "compass.py"]