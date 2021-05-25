FROM python:3.8
COPY . /back-end/app
WORKDIR /back-end/app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
cmd python ./back-end/app/app.py

