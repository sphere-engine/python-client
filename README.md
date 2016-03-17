## Requirements.
Python 2.7, 3.4 or 3.5 [![Build Status](https://travis-ci.org/sphere-engine/python-client.svg?branch=master)](https://travis-ci.org/sphere-engine/python-client)

## Sphere Engine SDK

```sh
python setup.py install
```

Or you can install from Github via pip:

```sh
pip install git+https://github.com/sphere-engine/python-client.git
```

Or you can install from PyPI:

```sh
pip install sphere-engine
```

To use the bindings, import the pacakge:

```python
import sphere_engine
```


## Getting Started

TODO

## Documentation

Usage:

```sh
from sphere_engine import CompilersClientV3
client = CompilersClientV3('<token>', '<endpoint>')
r = client.submissions.create('<source_code>', compilerId, '<input>')
print client.submissions.get(r['id'])

(...)
```