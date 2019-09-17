#!/usr/bin/env python3

from glob import glob
from os.path import dirname, basename
from urllib.parse import urlparse
import re
import subprocess

from pygls.server import LanguageServer
from pygls.features import (COMPLETION, TEXT_DOCUMENT_DID_CHANGE,
                            TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN,
                            WORKSPACE_DID_CHANGE_CONFIGURATION)
from pygls.types import (CompletionItem, CompletionList, CompletionParams,
                         ConfigurationItem, ConfigurationParams, Diagnostic,
                         DidChangeTextDocumentParams,
                         DidCloseTextDocumentParams, DidOpenTextDocumentParams,
                         Position, Range, DidChangeConfigurationParams)
from pygls.workspace import Document

from v1_0 import SchemaSaladException, ValidationException, load_document_by_string, load_document

server = LanguageServer()


@server.feature(COMPLETION, trigger_characters=[': ', '- '])
def completions(ls, params: CompletionParams):
    ls.show_message_log('cwlls: Start completion...')
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
    ls.show_message_log('cwlls: Start didChange...')
    ds = validate(ls, ls.workspace.get_document(params.textDocument.uri))
    ls.publish_diagnostics(params.textDocument.uri, ds)


@server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(ls, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    ls.show_message_log('cwlls: Start didClose...')


@server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    ls.show_message_log('cwlls: Start didOpen...')


@server.feature(WORKSPACE_DID_CHANGE_CONFIGURATION)
def did_change_configuration(ls, params: DidChangeConfigurationParams):
    ls.show_message_log('cwlls: Start didChangeConfiguration...')


def validate(ls, doc: Document):
    fname = doc.uri.replace('file://', '')
    try:
        # ret = load_document(fname, doc.uri)
        _ = load_document_by_string(doc.source, doc.uri)
    except ValidationException as e:
        str(e)
    return []
    # we should use the following instead of `load_document`
    # load_document_by_string(doc, doc.uri)
    # cwl_schema = '/path/to/schema.yml'
    # cwl_schema = '/Users/tom-tan/repos/common-workflow-language/v1.0/CommonWorkflowLanguage.yml'
    # cmd = ['schema-salad-tool', cwl_schema, fname, '--print-oneline']
    # ret = subprocess.run(cmd, stderr=subprocess.PIPE)
    # if ret.returncode != 0:
    #     output = ret.stderr.decode()

    #     ds = []
    #     for l in output.splitlines()[2:]:
    #         d = str2diagnostic(l, doc)
    #         if d:
    #             ds.append(d)

    #     return ds
    # else:
    #     return []


def str2diagnostic(s, doc):
    pat = re.compile("^.+?:(\d+):(\d+): (.+)$")
    match = pat.match(s)
    if match:
        line, column, msg = match.groups()
        line = int(line)
        column = int(column)
        return Diagnostic(range = Range(Position(line = line-1,
                                                 character = column-1),
                                        Position(line = line-1,
                                                 character = column)),
                          message = msg,
                          source = 'cwlls')
    else:
        return None


if __name__ == '__main__':
    server.start_io()
