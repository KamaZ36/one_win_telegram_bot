FROM python:3.11.6

VOLUME ./app

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

copy . .

CMD ["python3", "-u", "main.py"]
