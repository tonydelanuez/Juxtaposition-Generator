FROM python:3.7
ADD . /flaskapp
WORKDIR /flaskapp
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "flask" ]