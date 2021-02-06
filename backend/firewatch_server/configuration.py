from logging import getLogger
import os
from pathlib import Path
import yaml


logger = getLogger(__name__)

top_module_dir = Path(__file__).parent


class ConfigurationError (Exception):
    pass


class Configuration:

    def __init__(self, args):
        self.bind_host = args.bind or ''
        self.bind_port = int(args.port or 8000)
        cfg_path = args.conf or os.environ.get('CONF')
        if not cfg_path:
            raise ConfigurationError('Configuration path is not set - use --conf or CONF')
        cfg_path = Path(cfg_path)
        cfg_dir = cfg_path.parent
        cfg = yaml.safe_load(cfg_path.read_text())
        self.http_checks = [HTTPCheck(d) for d in cfg['http_checks']]
        logger.debug('Loaded %d HTTP checks from %s', len(self.http_checks), cfg_path)
        if os.environ.get('HTML_DIR'):
            self.html_dir = cfg_dir / os.environ.get['HTML_DIR']
        elif cfg.get('html_dir'):
            self.html_dir = cfg_dir / cfg['html_dir']
        else:
            self.html_dir = top_module_dir.parent.parent / 'frontend' / 'out'


class HTTPCheck:

    default_interval = 30 # in seconds

    def __init__(self, data):
        self.check_id = data.get('id') or data['url']
        self.url = data['url']
        self.interval = float(data.get('interval') or self.default_interval) # in seconds
        assert isinstance(self.check_id, str)
        assert isinstance(self.url, str)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.check_id!r} url={self.url!r}>"
