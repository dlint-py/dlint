from importlib.metadata import metadata

from . import linters  # noqa F401
from . import multi  # noqa F401
from . import namespace  # noqa F401
from . import redos  # noqa F401
from . import test  # noqa F401
from . import tree  # noqa F401
from . import util  # noqa F401

m = metadata('dlint')


def _homepage(package_metadata):
    homepage = package_metadata.get('Home-page')
    if homepage:
        return homepage

    for project_url in package_metadata.get_all('Project-URL', []):
        label, separator, url = project_url.partition(',')
        if separator and label.strip().lower() == 'homepage':
            return url.strip()

    return None


__name__ = m['Name']
__version__ = m['Version']
__description__ = m['Summary']
__url__ = _homepage(m)
__license__ = m['License']
