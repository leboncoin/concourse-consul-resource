# Concourse Hashicorp Consul Resource
A very handy [Concourse CI](http://concourse.ci) resource for watching and reacting to key/value changes in Hashicorp [Consul](https://www.consul.io/).

A typical use case for this would be:
* create a resource instance that watches a set of paths in Consul
* when something changes under the given set of paths (added/deleted/modified), you will get a resource ref
* all retrieved key/values are available to be used in Concourse tasks

Watching is done recursively, i.e. "all keys under /path1" and "all keys under /path2", etc. The resource basically retrieves
all key/value pairs from the given set of paths, and resource ref is a hash of key/value pairs sorted by key.
 
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
