#!/usr/bin/env python

from .helpers import bad_module_use


class BadXMLUseLinter(bad_module_use.BadModuleUseLinter):
    """This linter looks for use of the Python "xml" module EXCEPT defusedxml.
    Etree and Minidom are bad - using TreeBuilder is okay because it does not
    parse xml.
    """
    off_by_default = False

    _code = 'DUO107'
    _error_tmpl = 'DUO107 insecure use of XML modules, prefer "defusedxml"'

    @property
    def illegal_modules(self):
        return [
            'lxml',
            'xml',
            'xmlrpclib',
        ]

    @property
    def whitelisted_modules(self):
        return [
            'xml.sax.saxutils',
            'xml.etree.ElementTree.Element',
            'xml.etree.ElementTree.SubElement',
        ]
