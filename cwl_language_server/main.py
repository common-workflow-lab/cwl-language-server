#!/usr/bin/env python
import sys

import pylspclient

import callbacks

import logging
from logging import getLogger, StreamHandler, Formatter

logger = getLogger("CWLLSP")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="./cwl-language-server.log")
handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(handler_format)
logger.addHandler(handler)

logger.debug("Start CWL Language Server")

def main():
    stdin = sys.stdout.buffer
    stdout = sys.stdin.buffer
    json_rpc_endpoint = pylspclient.JsonRpcEndpoint(stdin, stdout)
    lsp_endpoint = pylspclient.LspEndpoint(json_rpc_endpoint,
                                           method_callbacks={
                                               'initialize': callbacks.initialize,
                                               'initialized': callbacks.initialized,
                                               'textDocument/completion': callbacks.completion,
                                           },
                                           notify_callbacks={
                                               'textDocument/didChange': callbacks.didChange,
                                           })
    lsp_endpoint.start()

if __name__ == '__main__':
    main()
