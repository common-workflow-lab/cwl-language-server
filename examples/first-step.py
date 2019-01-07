#!/usr/bin/env python
import os
import sys

import pylspclient
from pylspclient.lsp_structs import TextDocumentItem, Position, CompletionContext, CompletionTriggerKind
import cwl_language_server.callbacks as callbacks


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
                                           })
    client = pylspclient.LspClient(lsp_endpoint)
    print(client.initialize(processId=None, rootPath=None, rootUri=None,
                            initializationOptions=None, capabilities={},
                            trace=None, workspaceFolders=None),
          file=sys.stderr)
    print(client.initialized(), file=sys.stderr)
    print(client.completion(
        TextDocumentItem(None, 'cwl', 1, ''),
        Position(0, 0),
        CompletionContext(CompletionTriggerKind.Invoked)),
          file=sys.stderr)
    client.shutdown()
    client.exit()
    # BUG: Need ^C
