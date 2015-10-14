## Requirements.
Python 2.7 and later.

## Sphere Engine SDK

```sh
python setup.py install
```

Or you can install from Github via pip:

```sh
pip install git+https://github.com/sphere-engine/sphereengine-python.git
```

To use the bindings, import the pacakge:

```python
import sphere_engine
```


## Getting Started

TODO

## Documentation

Usage:
from sphere_engine import SphereEngine
api = SphereEngine('<token>', 'v3', '<endpoint>')
client = api.execution_client()
r = client.submissions.create('<source_code>', compilerId, '<input>')
print client.submissions.get(r['id'])

client = api.problems_client()
rrr = client.submissions.create('<problem_code>', '<source_code>', compilerId)
print client.submissions.get(r['id'])
