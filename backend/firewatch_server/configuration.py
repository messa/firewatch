from logging import getLogger
import os
from pathlib import Path
import re
from secrets import token_hex
import yaml


logger = getLogger(__name__)

top_module_dir = Path(__file__).parent


class ConfigurationError (Exception):
    pass


class Configuration:

    def __init__(self, args):
        cfg_path = args.conf or os.environ.get('CONF')
        if not cfg_path:
            raise ConfigurationError('Configuration path is not set - use --conf or CONF')
        cfg_path = Path(cfg_path)
        cfg_dir = cfg_path.parent
        cfg = yaml.safe_load(cfg_path.read_text())
        #self.http_checks = [HTTPCheck(d) for d in cfg['http_checks']]
        #logger.debug('Loaded %d HTTP checks from %s', len(self.http_checks), cfg_path)

        self.bind_host = args.bind or ''
        self.bind_port = int(args.port or 8000)

        self.session_secret = os.environ.get('SESSION_SECRET') or cfg.get('session_secret') or token_hex()

        if os.environ.get('STATIC_DIR'):
            self.static_dir = cfg_dir / os.environ['STATIC_DIR']
        elif cfg.get('static_dir'):
            self.static_dir = cfg_dir / cfg['static_dir']
        else:
            self.static_dir = top_module_dir.parent.parent / 'frontend' / 'out'

        self.projects = [Project(proj_name, proj_cfg) for proj_name, proj_cfg in cfg['projects'].items()]
        self.auth = Auth(cfg.get('auth') or {})

    def __repr__(self):
        return f"<{self.__class__.__name__} loaded from {str(cfg_path)!r}>"

    @property
    def session_secret_bytes(self):
        return self.session_secret.encode()

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


class Auth:

    def __init__(self, cfg):
        self.google_client_id = os.environ.get('GOOGLE_CLIENT_ID') or cfg.get('google_client_id')
        self.google_client_secret = os.environ.get('GOOGLE_CLIENT_SECRET') or cfg.get('google_client_secret')
        self.google_redirect_uri = cfg.get('google_redirect_uri')
        self.google_scope = [
            'openid',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
        ]
        self.google_authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
        self.google_fetch_token_url = 'https://www.googleapis.com/oauth2/v4/token'
        self.google_user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'


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
        self.raw_assigned_users = cfg.get('assigned_users') or []

    def __repr__(self):
        return f"<{self.__class__.__name__} project_id={self.check_id!r}>"

    def has_user_assigned(self, user):
        if not user:
            return False
        assert isinstance(user, dict)
        user_email = user.get('email')
        for item in self.raw_assigned_users:
            if item.keys() == {'email'}:
                item_email, = item.values()
                if user_email == item_email:
                    return True
            elif item.keys() == {'email_regex'}:
                item_regex, = item.values()
                if re.search(item_regex, user_email):
                    return True
            else:
                raise Exception(f"Could not interpret assigned_users configuration: {item!r}")
        return False


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
