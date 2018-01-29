FROM python:2.7.14
WORKDIR /code
ADD . .
RUN apt-get update && apt-get install bc
RUN pip install -r requirements.txt
CMD ["python", "app.py"]