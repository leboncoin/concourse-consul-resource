FROM python:2-alpine
COPY dist/concourse-consul-resource-*.tar.gz .
RUN pip install concourse-consul-resource-*.tar.gz
RUN mkdir -p /opt/resource
RUN for script in check in out; do ln -s $(which $script) /opt/resource/; done
