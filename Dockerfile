FROM python:3

WORKDIR /app

COPY . .

RUN pip install -r ../requirments.txt

CMD python -u ./main.py