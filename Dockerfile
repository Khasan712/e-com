FROM python:3.11

ENV PYTHONDONTWRITENYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . /app
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt
#EXPOSE 8000
#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "config.wsgi"]
