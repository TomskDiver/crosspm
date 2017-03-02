# -*- coding: utf-8 -*-
from urllib.request import urlopen, urljoin

import pytest
import json

# from . import assert_warn
from crosspm.adapters.artifactory import Adapter
from crosspm.helpers.config import Config

_adapter = None
_config = None


@pytest.fixture(scope='module')
def app():
    from tests.repo.artifactory.server import app
    return app


@pytest.mark.usefixtures('live_server')
class TestArtifactory:
    config_yaml = """
    cpm:
      description: Artifactory Adapter Test
      dependencies: dependencies.txt
      dependencies-lock: dependencies.txt.lock
      cache:
        cmdline: cache
        env: CROSSPM_CACHE_ROOT
        default:

    columns: "*package, version, branch, compiler, arch, osname"

    options:
      compiler:
        cmdline: cl
        env: CROSSPM_COMPILER
        default: any

      arch:
        cmdline: arch
        env: CROSSPM_ARCH
        default: any

      osname:
        cmdline: os
        env: CROSSPM_OS
        default: '450'

    defaults:
      branch: '*'

    solid:
      ext:
        - '*.deb'
        - '*.exe'
        - '*.msi'

    parsers:
      common:
        columns:
          version: "{int}.{int}.{int}[.{int}][-{str}]"
        sort:
          - version
          - '*'
        index: -1

      artifactory:
        path: "{server}/{repo}/{package}/{branch}/{version}/{compiler|any}/{arch|any}/{osname}/{package}.{version}[.zip|.tar.gz|.nupkg]"
        properties: ""

    fails:
      unique:
        - package
        - version

    sources:
      - server: http://localhost:5000/artifactory
        repo:
          - test_repo_1
        parser: artifactory
        type: jfrog-artifactory
        auth_type: simple
        auth:
          - login
          - password
    output:
      tree:
        - package: 25
        - version: 0
    """

    @pytest.fixture(scope='class', autouse=True)
    def set_mod(self, tmpdir_factory):
        global _adapter, _config

        path = tmpdir_factory.mktemp('data').join("crosspm.yaml")
        path.write(self.config_yaml)

        _config = Config(str(path))
        _adapter = _config._adapters.get('jfrog-artifactory', None)
        assert isinstance(_adapter, Adapter)

    def change_source(self, live_server):
        global _config
        if _config is not None:
            _sources = getattr(_config, '_sources', None)
            if (_sources is not None) and (isinstance(_sources, (list, tuple))):
                for _src in _sources:
                    _args = getattr(_src, 'args', None)
                    if (_args is not None) and (isinstance(_args, dict)):
                        _args['server'] = urljoin(live_server.url(), '/artifactory')

    def test__init(self, live_server):
        self.change_source(live_server)

        res = urlopen(live_server.url())
        res_data = json.loads(res.read().decode(encoding="utf-8"))
        assert res_data == {'success': True, 'message': 'Test API connection'}

        print(res)

    def test__artifactory(self, live_server):
        self.change_source(live_server)

        res = urlopen(urljoin(live_server.url(), '/artifactory'))
        res_data = json.loads(res.read().decode(encoding="utf-8"))
        assert res_data == {'success': True, 'message': 'Artifactory ROOT'}

        print(res)
