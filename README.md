# CWL-language-server

[![Build Status](https://travis-ci.org/common-workflow-language/cwl-language-server.svg?branch=master)](https://travis-ci.org/common-workflow-language/cwl-language-server)

# What is Language Server ?

[Langserver\.org](https://langserver.org/)

# Requirements

python3

# How to use

```console
$ pip install -r requirements.txt
```

## Install pylspclient

Currently, we must use `send-result-wip` branch of [yeger00/pylspclient: LSP client implementation in Python](https://github.com/yeger00/pylspclient/)

# How to execute example

```console
$ PYTHONPATH=/path/to/cwl-language-server python examples/first-step.py
```

## for example

```
PYTHONPATH=$PWD python examples/first-step.py
```

# How to stop example

`CTRL-c`
