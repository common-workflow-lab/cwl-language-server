#!/usr/bin/env python
import sys

import pylspclient

import callbacks

def main():
    stdin = sys.stdout
    stdout = sys.stdin
    json_rpc_endpoint = pylspclient.JsonRpcEndpoint(stdin, stdout)
    lsp_endpoint = pylspclient.LspEndpoint(json_rpc_endpoint, default_callback=print,
                                           callbacks={ 'completion': callbacks.completion })
    lsp_endpoint.run()

if __name__ == '__main__':
    main()
