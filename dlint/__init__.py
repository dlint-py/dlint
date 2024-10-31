from importlib.metadata import metadata

from . import linters  # noqa F401
from . import multi  # noqa F401
from . import namespace  # noqa F401
from . import redos  # noqa F401
from . import test  # noqa F401
from . import tree  # noqa F401
from . import util  # noqa F401

m = metadata('dlint')

__name__ = m['Name']
__version__ = m['Version']
__description__ = m['Summary']
__url__ = m['Home-page']
__license__ = m['License']
