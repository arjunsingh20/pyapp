FROM python:2.7.14
WORKDIR /code
ADD . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]