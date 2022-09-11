#!/usr/bin/env python

import abc

from .. import base


class BadBuiltinUseLinter(base.BaseLinter, abc.ABC):
    """This abstract base class provides a simple interface for creating new
    lint rules that block builtin functions.
    """
    @property
    @abc.abstractmethod
    def illegal_builtin(self):
        """Subclasses must implement this property to return a string of the
        builtin function name they'd like to blacklist.
        """

    def visit_Name(self, node):
        if (node.id == self.illegal_builtin
                and not self.namespace.name_imported(node.id)):
            self.results.append(
                base.Flake8Result(
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                    message=self._error_tmpl
                )
            )
