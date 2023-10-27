from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3.9/'
PEPS_URL = 'https://peps.python.org/'

BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = 'downloads'
lOG_DIR = BASE_DIR / 'logs'
lOG_FILE = lOG_DIR / 'parser.log'
RESULTS_DIR = 'results'
PRETTY_OUTPUT = 'pretty'
FILE_OUTPUT = 'file'

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
