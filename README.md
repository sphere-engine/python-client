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

## Full list of compilers

| Compiler  | Version |
| ------------- | ------------- |
| ADA 95 | 	gnat 5.1.1 |
| Assembler	 | NASM 2.11.05 |
| Awk | 	fawk 4.1.1 |
| Bash | 	bash 4.3.33 |
| Brainf**k | 	1.0.6 |
| C	 | gcc 5.1.1 |
| C# | 	Mono 4.0.2 |
| C++ | 	5.1.1 |
| C++ | 	g++ 4.3.2 |
| C99 strict | 	gcc-5 5.1.1 |
| Clips	clips |  6.24 |
| Clojure | 	clojure 1.7.0 |
| Common Lisp | 	sbcl 1.2.12 |
| Common Lisp | 	clisk 2.49 |
| D | 	gdc-5 5.1.1 |
| Erlang | 	erl 18 |
| F# | 	1.3 |
| Fortran 95 | 	5.1.1 |
| Go | 	1.4 |
| Haskell | 	ghc 7.8 |
| Icon | 	icon 9.4.3 |
| Intercal | 	ick 0.28-4 |
| JAR | 	java6 |
| Java | 	jdk 8u51 |
| Java 7 | 	java7 |
| Java Script | 	rhino 1.7.7 |
| Lua | 	lua 7.2 |
| Nemerle | 	ncc 0.9.3 |
| Nice | 	0.9.13 |
| Node.js | 	v0.12.7 |
| Ocaml | 	4.01.0 |
| PHP | 	PHP 5.6.11-1 |
| Pascal | 	gpc 20070904 |
| Pascal | 	fpc 2.6.4+dfsg-6 |
| Perl | 	perl 5.12.1 |
| Perl | 	perl6 2014.07 |
| Pike | 	pike v7.8 |
| Prolog | 	swi 7.2 |
| Python | 	2.7.10 |
| Python 3 | 	Python 3.4.3+ |
| Ruby | 	ruby 2.1.5 |
| SQL | 	0 |
| Scala | 	2.11.7 |
| Scheme | 	stalin 0.11 |
| Scheme | 	guile 1.8.5 |
| Sed | 	sed 4.2.2 |
| Smalltalk | 	gst 3.2.4 |
| Tcl | 	tclsh 8.5.3 |
| Text | 	plain text |
| Whitespace | 	wspace 0.3 |
