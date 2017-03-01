# -*- coding: utf-8 -*-
from urllib.request import urlopen

import pytest
import yaml
from flask import url_for, Flask

from . import assert_warn
from crosspm.adapters.artifactory import Adapter
from crosspm.helpers.config import Config

_adapter = None
_config = None


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

    # @pytest.fixture()
    # def app(self):
    #     from tests.repo.server import app
    #     return app

    # @pytest.fixture()
    # def app(self):
    #     app = Flask(__name__)
    #     return app

    # @pytest.mark.usefixtures('live_server')
    def test__init(self):  # , live_server):
        # live_server.start()
        #print(live_server.url())

        res = urlopen(url_for('artifactory', _external=True))
        # res = client.get('/')
        # assert res is not None
