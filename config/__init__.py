import os

env = os.getenv('ALPHA', 'dev')
if env == 'local':
    from .local_config import Configuration
if env == 'dev':
    from .dev_config import Configuration