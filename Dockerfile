FROM python:3
ENV PYTHONBUFFERED=0
WORKDIR /code
COPY requirments.txt /code/
RUN pip install -r requirments.txt
COPY . /code/
