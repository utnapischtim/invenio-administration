# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Administration core admin module."""

from flask_menu import current_menu

from invenio_administration.dashboard import AdminDashboardView
from invenio_administration.menu import AdminMenu


class Administration:
    """Admin views core manager."""

    def __init__(
        self,
        app=None,
        name=None,
        url=None,
        dashboard_view=None,
        ui_endpoint=None,
        base_template=None,
    ):
        """Constructor.

        :param app: flask application
        :param name: application name, defaults to "Admin"
        :param url: base admin url to register the dashboard view and subviews
        :param dashboard_view: home page view
        :param ui_endpoint: base UI endpoint,
                     leaves flexibility to implement two different admin apps,
                     or to provide custom endpoint
        :param base_template: base admin template.
                     Defaults to "admin/base.html"
        """
        super().__init__()

        self.app = app

        self._views = []
        self._menu = AdminMenu()
        self._menu_key = "admin_navigation"

        if name is None:
            name = "Administration"
        self.name = name

        self.dashboard_view = dashboard_view or AdminDashboardView(
            endpoint=ui_endpoint, url=url
        )
        # self.ui_endpoint = ui_endpoint or self.dashboard_view.endpoint
        self.ui_endpoint = ui_endpoint or "administration"
        self.url = url or self.dashboard_view.url
        self.url = url or "/administration"
        self.base_template = \
            base_template or "invenio_administration/base.html"

        if self.dashboard_view is not None:
            self._add_dashboard_view(
                dashboard_view=self.dashboard_view,
                endpoint=ui_endpoint, url=url
            )

        @app.before_first_request
        def init_menu():
            self._menu.register_menu_entries(current_menu, self._menu_key)

    def add_view(self, view, *args, **kwargs):
        """Add a view to the collection.

        :param view: View to add.
        """
        # Add to views
        self._views.append(view)

        # If app was provided in constructor, register view with Flask app
        if self.app is not None:
            self.app.register_blueprint(view.create_blueprint(self))

        self._menu.add_view_to_menu(view)

    def add_views(self, *args):
        """Add multiple views."""
        for view in args:
            self.add_view(view)

    def _add_dashboard_view(self,
                            dashboard_view=None, endpoint=None, url=None):
        """Add the admin index view.

        :param dashboard_view:
             Home page view to use. Defaults to `AdminIndexView`.
        :param url: Base URL.
        :param endpoint: Base endpoint name for index view.
            When using multiple instances of the `Admin` class in a flask app
            you have to set a unique endpoint name for each instance.
        """
        from invenio_administration.dashboard import AdminDashboardView

        self.dashboard_view = dashboard_view or AdminDashboardView(
            endpoint=endpoint, url=url
        )
        self.endpoint = endpoint or self.dashboard_view.endpoint
        self.url = url or self.dashboard_view.url

        # Add predefined index view
        # assume index view is always the first element of views.
        if len(self._views) > 0:
            self._views[0] = self.dashboard_view
            self._menu.add_view_to_menu(self.dashboard_view, index=0)
        else:
            self.add_view(self.dashboard_view)
