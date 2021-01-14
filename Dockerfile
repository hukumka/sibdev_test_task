FROM python:3
ENV PYTHONBUFFERED=1
WORKDIR /code
COPY requirments.txt /code/
RUN pip install -r requirments.txt
COPY . /code/
