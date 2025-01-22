FROM python:3.11

ENV PYTHONDONTWRITENYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY main.py /fast/
COPY requirements.txt /fast/
COPY . /fast
WORKDIR /fast
RUN pip install --upgrade pip && pip install -r requirements.txt
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8051"]
