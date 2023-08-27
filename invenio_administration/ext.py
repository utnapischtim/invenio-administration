# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio admin extension."""

from . import config


class InvenioAdministration:
    """Invenio extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        self.view_classes = []
        self.administration = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize application."""
        self.init_config(app)

        app.extensions["invenio-administration"] = self

    @staticmethod
    def init_config(app):
        """Initialize configuration.

        :param app: The Flask application.
        """
        # Set default configuration
        for k in dir(config):
            if k.startswith("ADMINISTRATION_"):
                app.config.setdefault(k, getattr(config, k))
