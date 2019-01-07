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

### Expected Result

Looks like this.

```console
$ python examples/first-step.py
{'capabilities': {'completionProvider': {'triggerCharacters': [': ']}}}
None
{'jsonrpc': '2.0', 'method': 'initialized', 'params': {}}
[{'label': 'draft-2', 'deprecated': True}, {'label': 'draft-3.dev1', 'deprecated': True}, {'label': 'draft-3.dev2', 'deprecated': True}, {'label': 'draft-3.dev3', 'deprecated': True}, {'label': 'draft-3.dev4', 'deprecated': True}, {'label': 'draft-3.dev5', 'deprecated': True}, {'label': 'draft-3', 'deprecated': True}, {'label': 'draft-4.dev1', 'deprecated': True}, {'label': 'draft-4.dev2', 'deprecated': True}, {'label': 'draft-4.dev3', 'deprecated': True}, {'label': 'v1.0.dev4', 'deprecated': True}, {'label': 'v1.0'}]
```

# How to stop example

`CTRL-c`



