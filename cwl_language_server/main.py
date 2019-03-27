#!/usr/bin/env python3

from glob import glob
from os.path import dirname, basename
from urllib.parse import urlparse

from pygls.server import LanguageServer
from pygls.features import (COMPLETION, TEXT_DOCUMENT_DID_CHANGE,
                            TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN,
                            WORKSPACE_DID_CHANGE_CONFIGURATION)
from pygls.types import (CompletionItem, CompletionList, CompletionParams,
                         ConfigurationItem, ConfigurationParams, Diagnostic,
                         DidChangeTextDocumentParams,
                         DidCloseTextDocumentParams, DidOpenTextDocumentParams,
                         Position, Range, DidChangeConfigurationParams)

server = LanguageServer()


@server.feature(COMPLETION, trigger_characters=[': ', '- '])
def completions(ls, params: CompletionParams):
    ctx = params.context
    line = params.position.line
    col = params.position.character
    uri = params.textDocument.uri

    doc = ls.workspace.get_document(params.textDocument.uri)

    field = doc.lines[line][0:col].lstrip().rstrip(': ')
    if not field:
        return CompletionList(False, [])

    if field in completion_list:
        return completion_list[field]
    if field == 'run':
        cwls = glob("{}/*.cwl".format(dirname(urlparse(uri).path)))
        return [CompletionItem(basename(cwl))
                for cwl in cwls if cwl != urlparse(uri).path]
    return CompletionList(False, [])


completion_list = {
    'cwlVersion': [
        CompletionItem('draft-2',      deprecated=True),
        CompletionItem('draft-3.dev1', deprecated=True),
        CompletionItem('draft-3.dev2', deprecated=True),
        CompletionItem('draft-3.dev3', deprecated=True),
        CompletionItem('draft-3.dev4', deprecated=True),
        CompletionItem('draft-3.dev5', deprecated=True),
        CompletionItem('draft-3',      deprecated=True),
        CompletionItem('draft-4.dev1', deprecated=True),
        CompletionItem('draft-4.dev2', deprecated=True),
        CompletionItem('draft-4.dev3', deprecated=True),
        CompletionItem('v1.0.dev4',    deprecated=True),
        CompletionItem('v1.0'),
    ],
}


@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    pass


@server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(server, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    pass


@server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    pass


@server.feature(WORKSPACE_DID_CHANGE_CONFIGURATION)
def did_change_configuration(ls, params: DidChangeConfigurationParams):
    pass


if __name__ == '__main__':
    server.start_io()
