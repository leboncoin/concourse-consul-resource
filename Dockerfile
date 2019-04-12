FROM python:2-alpine

WORKDIR /install
COPY . /install/
RUN python setup.py install

# Move files to match concourse norme
RUN mkdir -p /opt/resource
RUN for script in check in out; do ln -s $(which $script) /opt/resource/; done

# clean install files
RUN rm -rf /install

WORKDIR /opt/resource
CMD [ "/bin/sh" ]
