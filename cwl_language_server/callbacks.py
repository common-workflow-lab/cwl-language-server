#!/usr/bin/env python
from pylspclient.lsp_structs import CompletionList

capabilities = {
    'completionProvider': {
        'triggerCharacters': [':'],
    },
}

def completion(params): # CompletionParams -> CompletionList
    print(params)
    ctx = params.context
    pos = params.position
    uri = params.textDocument.uri
    return CompletionList(False, [])

if __name__ == '__main__':
    pass
