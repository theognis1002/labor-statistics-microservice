FROM python:3.8-buster
ENV FLASK_APP=app
ENV FLASK_ENV=development
COPY . /src
WORKDIR /src
RUN apt-get update && \
    apt-get -y install python3-pandas
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]
