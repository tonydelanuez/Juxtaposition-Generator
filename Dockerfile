FROM python:3.7
USER root

# Set user and group
ARG user=juxgen
ARG group=juxgen
ARG uid=1000
ARG gid=1000
RUN groupadd -g ${gid} ${group}
RUN useradd -u ${uid} -g ${group} -s /bin/sh -m ${user}

USER ${user}
ADD . /home/${user}/flaskapp
WORKDIR /home/${user}/flaskapp
RUN pip install -r requirements.txt

EXPOSE 5000