FROM python:3.10-alpine

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY *.py ./

CMD python main.py