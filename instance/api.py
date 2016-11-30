import inspect
import functools
import six

from docker import client
from docker import tls

DEFAULT_TIMEOUT_SECONDS = 120
DEFAULT_DOCKER_API_VERSION = '1.19'

def filter_data(f):
    """Decorator that post-processes data returned by Docker.
     This will avoid any surprises with different versions of Docker.
    """
    @functools.wraps(f, assigned=[])
    def wrapper(*args, **kwds):
        out = f(*args, **kwds)

        def _filter(obj):
            if isinstance(obj, list):
                new_list = []
                for o in obj:
                    new_list.append(_filter(o))
                obj = new_list
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(k, six.string_types):
                        obj[k.lower()] = _filter(v)
            return obj
        return _filter(out)
    return wrapper

class DockerHTTPClient(client.Client):
    def __init__(self, url='unix://var/run/docker.sock'):
        ssl_config = False
        client_cert = None
        
        super(DockerHTTPClient, self).__init__(
            base_url=url,
            version=DEFAULT_DOCKER_API_VERSION,
            timeout=DEFAULT_TIMEOUT_SECONDS,
            tls=ssl_config
        )
        self._setup_decorators()

    def _setup_decorators(self):
        for name, member in inspect.getmembers(self, inspect.ismethod):
            if not name.startswith('_'):
                setattr(self, name, filter_data(member))

    def pause(self, container_id):
        url = self._url("/containers/{0}/pause".format(container_id))
        res = self._post(url)
        return res.status_code == 204

    def unpause(self, container_id):
        url = self._url("/containers/{0}/unpause".format(container_id))
        res = self._post(url)
        return res.status_code == 204

    def load_repository_file(self, name, path):
        with open(path, 'rb') as fh:
            self.load_image(fh)

    def get_container_logs(self, container_id):
        return self.attach(container_id, 1, 1, 0, 1)


class DockerDriver:
    def __init__(self):
        self._docker = None
        
    @property
    def docker(self):
        if self._docker is None:
            self._docker = DockerHTTPClient()
        return self._docker

    def init_host(self, host):
        if self._is_daemon_running() is False:
            raise exception.NovaException(
                _('Docker daemon is not running or is not reachable'
                  ' (check the rights on /var/run/docker.sock)'))

    def _is_daemon_running(self):
        return self.docker.ping()

    def list_instances(self, inspect=False):
        res = []
        for container in self.docker.containers(all=True):
            info = self.docker.inspect_container(container['id'])
            print info, '====================================='
            if not info:
                continue
            if inspect:
                res.append(info)
            else:
                res.append(info['Config'].get('Hostname'))
        return res

    def list_instances_table(self):
        res = []
        for container in self.docker.containers(all=True):
            info = self.docker.inspect_container(container['id'])
            if not info:
                continue
            
            container_row = {
                "id": info['Config'].get('Hostname'),
                "hostname": info['Config'].get('Hostname'), 
                "image": info['Config'].get('image'), 
                "name": info['Config'].get('image'), 
                "status": 'N/A', 
                "port": 'N/A', 
            }

            res.append(container_row)
        return res