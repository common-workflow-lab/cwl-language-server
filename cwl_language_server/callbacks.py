#!/usr/bin/env python
import pylspclient.lsp_structs as structs

from glob import glob
from os.path import dirname, basename
import sys
from urllib.parse import urlparse

CONTENTS = {} # Hash[uri, Hash[string, Union[integer, TextContent]]]

class TextContent:
    # TODO: it should be tested
    def __init__(self, text): # Text -> self
        self.text = text.split("\n")

    def __getitem__(self, i): # integer -> string
        return self.text[i]

    def __str__(self): # None -> string
        return "\n".join(self.text)

    def remove_text(self, rng): # Range -> None
        stline = rng['start']['line']
        stcol = rng['start']['character']
        enline = rng['end']['line']
        encol = rng['end']['character']

        before = self.text[stline][:stcol]
        after = self.text[enline][encol:]

        self.text[stline] = before+after
        for _ in range(enline-stline):
            self.text.pop(stline+1)

    def insert_text(self, beg, text): # Position -> Text -> None
        stline = beg['line']
        stcol = beg['character']

        before = self.text[stline][:stcol]
        after = self.text[stline][stcol:]
        lines = text.split("\n")

        self.text[stline] = before+lines[0]
        idx = stline+1
        for l in lines[1:]:
            self.text.insert(idx, l)
            idx += 1
        self.text[idx-1] += after

def initialize(params): # InitializeParams -> InitializeResult
    return {
        'capabilities': {
            'textDocumentSync': {
                'openClose': True,
                'change': 2,
            },
            'completionProvider': {
                'triggerCharacters': [': ', '- '],
            },
        },
    }

def initialized(params): # InitializedParams -> None
    pass

def didChangeConfiguration(params): # ConfigurationParams -> None
    pass

def didOpen(params): # DidOpenTextDocumentParams -> None
    uri = params['textDocument']['uri']
    text = params['textDocument']['text']
    # print('Contents for {} is added.'.format(uri), file=sys.stderr)
    CONTENTS[uri] = {
        'version': 0,
        'text': TextContent(text),
    }

def didClose(params): # DidCloseTextDocumentParams -> None
    # print('Contents for {} is removed.'.format(params['uri']), file=sys.stderr)
    del CONTENTS[params['uri']]

def didChange(params): # DidChangeTextDocumentParams -> None
    uri = params['textDocument']['uri']
    version = params['textDocument']['version']
    changes = params['contentChanges']

    if version is None:
        pass # warning
    elif CONTENTS[uri]['version']+len(changes) != version:
        pass # warning

    wholetxt = CONTENTS[uri]['text']
    for ch in changes:
        txt = ch['text']
        if ch['range'] is None:
            CONTENTS[uri] = {
                'text': TextContent(txt),
                'version': 0,
            }
            wholetxt = CONTENTS[uri]['text']
            continue

        wholetxt.remove_text(ch['range'])
        wholetxt.insert_text(ch['range']['start'], txt)

def completion(params): # CompletionParams -> CompletionList
    # print('Params: ', params, file=sys.stderr)
    ctx = params.get('context', {})
    line = params['position']['line']
    col = params['position']['character']
    uri = params['textDocument']['uri']

    # print('Keys: ', CONTENTS.keys(), file=sys.stderr)
    field = CONTENTS[uri]['text'][line][0:col].lstrip().rstrip(': ')
    if not field:
        return structs.CompletionList(False, [])

    if field in completion_list:
        return completion_list[field]
    if field == 'run':
        cwls = glob("{}/*.cwl".format(dirname(urlparse(uri).path)))
        return [structs.CompletionItem(basename(cwl)) for cwl in cwls if cwl != urlparse(uri).path]
    return structs.CompletionList(False, [])

completion_list = {
    'cwlVersion': [
        structs.CompletionItem('draft-2',      deprecated=True),
        structs.CompletionItem('draft-3.dev1', deprecated=True),
        structs.CompletionItem('draft-3.dev2', deprecated=True),
        structs.CompletionItem('draft-3.dev3', deprecated=True),
        structs.CompletionItem('draft-3.dev4', deprecated=True),
        structs.CompletionItem('draft-3.dev5', deprecated=True),
        structs.CompletionItem('draft-3',      deprecated=True),
        structs.CompletionItem('draft-4.dev1', deprecated=True),
        structs.CompletionItem('draft-4.dev2', deprecated=True),
        structs.CompletionItem('draft-4.dev3', deprecated=True),
        structs.CompletionItem('v1.0.dev4',    deprecated=True),
        structs.CompletionItem('v1.0'),
    ],
}

def to_dict(obj):
    """Return a dictionary object for obj.
    All the fields with None values are omitted.
    It is used for debugging purpose."""
    if obj is None:
        return obj
    if isinstance(obj, list):
        return [to_dict(o) for o in obj if o is not None]
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, object):
        return { k:v for k, v in obj.__dict__.items() if v is not None }
    return obj

if __name__ == '__main__':
    pass
