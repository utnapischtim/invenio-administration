# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio admin extension."""

import importlib_metadata

from . import config
from .admin import Administration


class InvenioAdministration:
    """Invenio extension."""

    def __init__(self, app=None, entry_point_group="invenio_administration.views"):
        """Extension initialization."""
        self.entry_point_group = entry_point_group

        self.administration = None
        self._views = []
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize application."""
        self.init_config(app)
        self.administration = Administration(
            app,
            name=app.config["ADMINISTRATION_APPNAME"],
            base_template=app.config["ADMINISTRATION_BASE_TEMPLATE"],
        )
        if self.entry_point_group:
            self.load_entry_point_group(app)
        app.extensions["invenio-administration"] = self

    def load_entry_point_group(self, app):
        """Load admin interface views from entry point group."""
        entrypoints = set(importlib_metadata.entry_points(group=self.entry_point_group))
        for ep in entrypoints:
            admin_ep = ep.load()
            self.register_view(admin_ep, self._normalize_entry_point_name(ep.name), app)
        app.register_blueprint(self.administration.blueprint)

    def register_view(self, view_class, extension_name, app, *args, **kwargs):
        """Register an admin view on this admin instance.

        :param view_class: The view class name passed to the view factory.
        :param extension_name: The name of the extension which registered the view.
        :param args: Positional arguments for view class.
        :param kwargs: Keyword arguments to view class.
        """
        view_instance = view_class(
            extension=extension_name, admin=self.administration, *args, **kwargs
        )
        view = view_class.as_view(
            view_class.name,
            extension=extension_name,
            admin=self.administration,
            *args,
            **kwargs
        )
        self._views.append(view_class)
        self.administration.add_view(view, view_instance, *args, **kwargs)
        self.register_resource(app, view_class, extension_name)

    def register_resource(self, app, view_class, extension_name):
        """Set views schema."""

        @app.before_first_request
        def register_view_resource():
            if view_class.resource_config:
                view_class.set_resource(extension=extension_name)
            if view_class.schema:
                view_class.set_schema(extension=extension_name)

    @staticmethod
    def _normalize_entry_point_name(entry_point_name):
        return entry_point_name.replace("_", "-")

    @staticmethod
    def init_config(app):
        """Initialize configuration.

        :param app: The Flask application.
        """
        # Set default configuration
        for k in dir(config):
            if k.startswith("ADMINISTRATION_"):
                app.config.setdefault(k, getattr(config, k))
