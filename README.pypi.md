Uploading Project to PyPI
-------------------------

0. pip install twine; apt-get install twine
0. cp .pypirc.dist ~/.pypirc
0. edit ~/.pypirc

1. python setup.py sdist bdist_wheel
2. twine upload dist/*
