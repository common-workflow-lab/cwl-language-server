#!/usr/bin/env python
import sys

import pylspclient

import callbacks

def main():
    stdin = sys.stdout.buffer
    stdout = sys.stdin.buffer
    json_rpc_endpoint = pylspclient.JsonRpcEndpoint(stdin, stdout)
    lsp_endpoint = pylspclient.LspEndpoint(json_rpc_endpoint,
                                           method_callbacks={
                                               'initialize': callbacks.initialize,
                                               'textDocument/completion': callbacks.completion,
                                           },
                                           notify_callbacks={
                                               'initialized': callbacks.initialized,
                                               'workspace/didChangeConfiguration': callbacks.didChangeConfiguration,
                                               'textDocument/didOpen': callbacks.didOpen,
                                               'textDocument/didChange': callbacks.didChange,
                                               'textDocument/didClose': callbacks.didClose,
                                           })
    lsp_endpoint.start()

if __name__ == '__main__':
    main()
