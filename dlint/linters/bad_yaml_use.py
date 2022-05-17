#!/usr/bin/env python

from .helpers import bad_module_attribute_use


class BadYAMLUseLinter(bad_module_attribute_use.BadModuleAttributeUseLinter):
    """This linter looks for unsafe use of the Python "yaml" module. Its
    parsing functions (dump, dump_all, load, load_all) should be avoided in
    favor of their safe_* equivalent.
    """
    off_by_default = False

    _code = 'DUO109'
    _error_tmpl = 'DUO109 insecure use of "yaml" parsing function, prefer "safe_*" equivalent'

    @property
    def illegal_module_attributes(self):
        return {
            'yaml': [
                'dump',
                'dump_all',
                'load',
                'load_all',
            ],
        }
