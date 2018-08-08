#!/usr/bin/env python

# Copyright (c) 2018 Aptomi, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import sys
import hashlib
import consulate
import common
import os
import errno

def in_(destdir, instream):
    input = json.load(instream)

    # take snapshot of consul key/values
    consul_instance = consulate.Consul(host=input['source']['host'], port=input['source'].get('port', 443), scheme=input['source'].get('scheme', 'https'), token=input['source']['token'])

    # collect all keys from all given prefixes
    prefixes = input['source']['prefixes']
    if not isinstance(prefixes, (list,)):
        common.msg("[in] consul resource expected a list of prefixes, but it's not a list")
        exit(1)

    prefixStr = ""
    for prefix in prefixes:
        if len(prefixStr) > 0:
            prefixStr += " "
        prefixStr += prefix

    common.msg("[in] consul resource searching under {0}".format(prefixStr))

    result = {}
    for prefix in prefixes:
        found = consul_instance.kv.find(prefix)
        if found is not None:
            for k, v in found.iteritems():
                if v is not None:
                    result[k] = v
                else:
                    result[k] = ""

    common.msg("[in] consul resource found {0} key/values under {1}".format(len(result), prefixStr))

    # hash values from all keys
    hash = hashlib.sha224()
    for k, v in sorted(result.iteritems()):
        hash.update(v.encode("utf-8"))
    hashNew = hash.hexdigest()
    common.msg("[in] consul resource value hash under {0}: {1}".format(prefixStr, hashNew))

    # see if the same as previous version, or different
    version = input.get('version')
    hashRequested = version.get('hash', "") if version is not None else ""
    if hashRequested != hashNew:
        common.msg("[in] some values got changed in consul, so let's just fetch newer values")

    # put on a file system
    common.msg("[in] consul resource writing key/values to {0}".format(destdir))
    for k, v in result.iteritems():
        with safe_open(os.path.join(destdir, k), 'w') as f:
            f.write(v.encode("utf-8"))

    metadata = [{'name': 'keys', "value": str(len(result))}]
    return {'version': {'hash': hashNew}, 'metadata': metadata}

def safe_open(path, mode):
    mkdir_p(os.path.dirname(path))
    return open(path, mode)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def main():
    print(json.dumps(in_(sys.argv[1], sys.stdin)))

if __name__ == '__main__':
    main()
