# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Administration core admin module."""


from werkzeug.utils import import_string

from .views.base import AdminFormView, AdminResourceDetailView, AdminView


class Administration:
    """Admin views core manager."""

    def __init__(
        self,
        menu=None,
        name=None,
        url=None,
        ui_endpoint=None,
        base_template=None,
        dashboard_config=None,
    ):
        """Construct.

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

        self._views = []
        self._menu = menu

        if name is None:
            name = "Administration"
        self.name = name

        self.dashboard_view_class = self._load_admin_dashboard(dashboard_config)
        self.endpoint = ui_endpoint or "administration"
        self.url = url or "/administration"
        self.base_template = base_template or "invenio_administration/base.html"

        if self.dashboard_view_class is not None:
            self._add_dashboard_view()

    @property
    def views(self):
        """Registered admin views."""
        return self._views

    def add_view(self, view, view_instance):
        """Add a view to admin views."""
        # Validate view's class and name's uniqueness.
        if not issubclass(view.view_class, AdminView):
            msg = f"View class must be of type {AdminView.__name__}"
            raise TypeError(msg)
        if any(v.view_class.name == view.view_class.name for v in self.views):
            msg = f"View name already registered: {view.view_class.name}"
            raise ValueError(msg)

        self.views.append(view)

        if not isinstance(view_instance, AdminResourceDetailView) and not isinstance(
            view_instance,
            AdminFormView,
        ):
            self._menu.add_view_to_menu(view_instance)

    def _load_admin_dashboard(self, dashboard_config):
        """Load dashboard view configuration."""
        return import_string(dashboard_config)

    def _add_dashboard_view(self):
        """Add the admin dashboard view."""
        dashboard_instance = self.dashboard_view_class(
            admin=self, extension_name="invenio-administration"
        )
        dashboard_view = self.dashboard_view_class.as_view(
            self.dashboard_view_class.name,
            admin=self,
            extension_name="invenio-administration",
        )

        self.add_view(dashboard_view, dashboard_instance)
