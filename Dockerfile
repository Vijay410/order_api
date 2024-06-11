FROM python:3.7-slim-buster
RUN apt update -y && apt install awscli -y
WORKDIR /order_api
COPY . /order_api
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]
