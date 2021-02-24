## Requirements.
Python 2.7, 3.4+ [![Build Status](https://travis-ci.org/sphere-engine/python-client.svg?branch=master)](https://travis-ci.org/sphere-engine/python-client)

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

To use the bindings, import the package:

```python
import sphere_engine
```


## Unit tests

```python
./test.sh
```

## Examples

Usage:

```python
from sphere_engine import CompilersClientV4
client = CompilersClientV4('<token>', '<endpoint>')
r = client.submissions.create('<source_code>', compilerId, '<input>')
print(client.submissions.get(r['id']))

(...)
```

You will find many examples in the _Examples_ folder.

## Full list of compilers

A full list of programming languages is available at
[https://developer.sphere-engine.com/other/languages](https://developer.sphere-engine.com/other/languages).
