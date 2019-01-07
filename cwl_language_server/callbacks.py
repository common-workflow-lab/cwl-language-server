#!/usr/bin/env python
from pylspclient.lsp_structs import CompletionList
import sys

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
    # print('Params: ', params, file=sys.stderr)
    params = params['params']
    ctx = params['context']
    pos = params['position']
    uri = params['textDocument']['uri']
    return CompletionList(False, [])

if __name__ == '__main__':
    pass
