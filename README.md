# Concourse Hashicorp Consul Resource
A [Concourse CI](http://concourse.ci) resource for watching key/value changes in Hashicorp [Consul](https://www.consul.io/).

Docker image: https://hub.docker.com/r/aptomi/concourse-consul-resource

## Source Configuration
* `host`: *Required* Hostname or IP address of Consul
* `port`: *Optional, default `443`* Consul port
* `scheme`: *Optional, default `https`* Consul scheme
* `token`: *Required* Consul token to use
* `prefixes`: *Required* List of prefixes in Consul to watch. It will watch for changes in all keys starting with these prefixes

### Example
``` yaml
resource_types:
- name: consul-hash
  type: docker-image
  source:
    repository: aptomi/concourse-consul-resource

resources:
- name: consul
  type: consul-hash
  source:
    host: consul.mycompany.com
    token: f710a920-bb12-b356-ea1f-80f85f88f80b
    prefixes:
    - "aaa/bbb/ccc/ddd"
    - "aaa/bbb/eee"
    - "xxx/zzz"
```

## `get`: Download the latest version
No parameters.

## Development
To build the docker image for the resource:
``` sh
python setup.py sdist
docker build -t <username>/concourse-consul-resource .
```
