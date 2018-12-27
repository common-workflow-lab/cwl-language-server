#!/usr/bin/env python
from pylspclient.lsp_structs import CompletionList

def initialize(params): # InitializeParams -> InitializeResult
    return {
        'capabilities': {
            'completionProvider': {
                'triggerCharacters': [':'],
            },
        },
    }

def initialized(params): # InitializedParams -> None
    return

def completion(params): # CompletionParams -> CompletionList
    print(params)
    ctx = params.context
    pos = params.position
    uri = params.textDocument.uri
    return CompletionList(False, [])

if __name__ == '__main__':
    pass
