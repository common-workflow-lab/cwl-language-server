#!/usr/bin/env python
import os
import sys

import pylspclient
from pylspclient.lsp_structs import TextDocumentItem, Position, CompletionContext, CompletionTriggerKind, to_type, VersionedTextDocumentIdentifier, TextDocumentContentChangeEvent
import cwl_language_server.callbacks as callbacks

def print_response(resp):
    print(callbacks.to_dict(resp), file=sys.stderr)

if __name__ == '__main__':
    pipein, pipeout = os.pipe()
    pipein = os.fdopen(pipein, 'rb')
    pipeout = os.fdopen(pipeout, 'wb')
    json_rpc_endpoint = pylspclient.JsonRpcEndpoint(pipeout, pipein)
    lsp_endpoint = pylspclient.LspEndpoint(json_rpc_endpoint,
                                           method_callbacks={
                                               'initialize': callbacks.initialize,
                                               'initialized': callbacks.initialized,
                                               'textDocument/completion': callbacks.completion,
                                           },
                                           notify_callbacks={
                                               'textDocument/didChange': callbacks.didChange,
                                           },
                                               )
    client = pylspclient.LspClient(lsp_endpoint)
    print_response(client.initialize(processId=None, rootPath=None, rootUri=None,
                                     initializationOptions=None, capabilities={},
                                     trace=None, workspaceFolders=None))
    print_response(client.initialized())
    print_response(client.completion(
        TextDocumentItem('echo.cwl', 'cwl', 1, ''),
        Position(1, 12),
        CompletionContext(CompletionTriggerKind.Invoked)))
    print_response(client.didChange(
        VersionedTextDocumentIdentifier('echo.cwl', 1),
        TextDocumentContentChangeEvent(None,None,"cwlVersion: ")))
    print_response(client.shutdown())
    print_response(client.exit())
    # BUG: Need ^C
