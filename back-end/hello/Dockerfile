FROM python:3.8
#RUN apt-get update -y
#RUN apt-get install -y python-pip python-dev build-essential
#COPY . /app
#WORKDIR /app
#RUN pip install -r requirements.txt
#RUN python3 -m pip install --upgrade pip
#ENTRYPOINT ["python"]
#CMD ["hello.py"]
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install scikit-learn
RUN pip install -U spacy
RUN pip install tensorflow
RUN pip install nltk
RUN python -m spacy download en
RUN pip install matplotlib
RUN pip install seaborn
#RUN python -m pip install -U pytest
RUN pip install cufflinks
#RUN pip install collections
RUN pip install numpy
RUN pip install yake
#RUN pip install csv

RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["hello.py"]
