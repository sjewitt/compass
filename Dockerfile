FROM python:3.10

# location in the container
WORKDIR /code

# copy the reqs to working dir:
COPY ./requirements.txt /code/requirements.txt

# put the reqs in the container:
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy the application code to working dir in container
COPY . /code

CMD ["python", "compass.py", "--port", "80"]