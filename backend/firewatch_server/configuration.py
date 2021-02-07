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
        #self.http_checks = [HTTPCheck(d) for d in cfg['http_checks']]
        #logger.debug('Loaded %d HTTP checks from %s', len(self.http_checks), cfg_path)

        if os.environ.get('STATIC_DIR'):
            self.static_dir = cfg_dir / os.environ['STATIC_DIR']
        elif cfg.get('static_dir'):
            self.static_dir = cfg_dir / cfg['static_dir']
        else:
            self.static_dir = top_module_dir.parent.parent / 'frontend' / 'out'
        self.projects = [Project(proj_name, proj_cfg) for proj_name, proj_cfg in cfg['projects'].items()]

    def __repr__(self):
        return f"<{self.__class__.__name__} loaded from {str(cfg_path)!r}>"

    def get_project(self, project_id):
        for p in self.projects:
            if p.project_id == project_id:
                return p
        return None

    def get_check(self, check_id):
        p = self.get_project(check_id.split(':')[0])
        for ch in p.http_checks:
            if ch.check_id == check_id:
                return ch
        return None


class Project:

    def __init__(self, name, cfg):
        assert isinstance(name, str)
        logger.debug('Loading configuration for project %s', name)
        if ':' in name:
            raise ConfigurationError(f"Project name {name!r} cannot contain character ':'")
        self.name = name
        self.project_id = name
        self.title = cfg.get('title') or name
        self.http_checks = [HTTPCheck(self, check_name, check_cfg) for check_name, check_cfg in cfg['http_checks'].items()]

    def __repr__(self):
        return f"<{self.__class__.__name__} project_id={self.check_id!r}>"


class HTTPCheck:

    check_type = 'http_check'
    default_interval = 30 # in seconds

    def __init__(self, project, name, cfg):
        assert isinstance(name, str)
        if ':' in name:
            raise ConfigurationError(f"Check name {name!r} cannot contain character ':'")
        self.project = project
        self.name = name
        self.check_id = project.project_id + ':' + name
        self.url = cfg['url']
        self.interval = float(cfg.get('interval') or self.default_interval) # in seconds
        assert isinstance(self.check_id, str)
        assert isinstance(self.url, str)

    def __repr__(self):
        return f"<{self.__class__.__name__} check_id={self.check_id!r} url={self.url!r}>"
