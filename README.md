# CWL-language-server

[![Build Status](https://travis-ci.org/common-workflow-language/cwl-language-server.svg?branch=master)](https://travis-ci.org/common-workflow-language/cwl-language-server)

# What is Language Server ?

For details, see [Langserver\.org](https://langserver.org/).

# Requirements

- Python3
- master branch of [yeger00/pylspclient: LSP client implementation in Python](https://github.com/yeger00/pylspclient/)

# How to setup

```console
$ git clone https://github.com/common-workflow-language/cwl-language-server.git
$ cd cwl-language-server
$ pip install -r requirements.txt
```

# How to execute example

```console
$ git clone https://github.com/common-workflow-language/cwl-language-server.git
$ cd cwl-language-server
$ pip install -r requirements.txt
$ PYTHONPATH=$PWD python examples/first-step.py
{'capabilities': {'completionProvider': {'triggerCharacters': [': ']}}}
None
{'jsonrpc': '2.0', 'method': 'initialized', 'params': {}}
[{'label': 'draft-2', 'deprecated': True}, {'label': 'draft-3.dev1', 'deprecated': True}, {'label': 'draft-3.dev2', 'deprecated': True}, {'label': 'draft-3.dev3', 'deprecated': True}, {'label': 'draft-3.dev4', 'deprecated': True}, {'label': 'draft-3.dev5', 'deprecated': True}, {'label': 'draft-3', 'deprecated': True}, {'label': 'draft-4.dev1', 'deprecated': True}, {'label': 'draft-4.dev2', 'deprecated': True}, {'label': 'draft-4.dev3', 'deprecated': True}, {'label': 'v1.0.dev4', 'deprecated': True}, {'label': 'v1.0'}]
```

Use `CTRL-c` to exit the example.

# Example: Emacs with [Eglot](https://github.com/joaotavora/eglot)

- Install Eglot via package manager such as package.el
- Configure Eglot for cwl-language-server
  - Add the following to `init.el`:
```elisp
(require 'eglot)
(add-to-list 'eglot-server-programs
             '(cwl-mode . ("/path/to/python" "/path/to/cwl-language-server/cwl_language_server/main.py")))
(add-hook 'cwl-mode-hook 'eglot-ensure)
```
- Open CWL file
- Set the cursor after `cwlVersion: `
- If you installed `company.el`, possible versions are listed in the completion list. Otherwise use `M-x completion-at-point` or `M-x company-complete` by hand.
- Have fun!
