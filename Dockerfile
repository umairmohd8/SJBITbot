# syntax=docker/dockerfile:1

FROM python:3.8

ENV PYTHONUNBUFFERED 1


WORKDIR /disbot


ENTRYPOINT ["python"]
CMD ["bot.py"]

COPY requirements.txt ./ 

RUN pip install -r requirements.txt

COPY . .

