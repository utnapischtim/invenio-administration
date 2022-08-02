# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# invenio-administration is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""
import pytest
from flask import Flask
from flask_babelex import Babel
from flask_menu import Menu

from invenio_administration import InvenioAdministration


@pytest.fixture(scope="module")
def celery_config():
    """Override pytest-invenio fixture.

    TODO: Remove this fixture if you add Celery support.
    """
    return {}


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""

    def factory(**config):
        app = Flask("testapp", instance_path=instance_path)
        app.config.update(**config)
        Babel(app)
        InvenioAdministration(app)
        Menu(app)

        return app

    return factory


@pytest.fixture(scope="module")
def current_app(create_app):
    """Flask instance."""
    return create_app()


@pytest.fixture(scope="module")
def current_admin_menu(current_app):
    """Current Admin flask menu instance."""
    return current_app.extensions['menu']


@pytest.fixture(scope="module")
def current_admin_ext(current_app):
    """Current invenio-administration extension."""
    return current_app.extensions['invenio-administration']


@pytest.fixture(scope="module")
def current_admin_app(current_admin_ext):
    """Current Admin instance."""
    return current_admin_ext.administration
