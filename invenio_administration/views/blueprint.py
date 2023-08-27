# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Administration views blueprint."""

import importlib_metadata
from flask import Blueprint
from invenio_theme import menu

from ..admin import Administration
from ..menu import AdminMenu
from .base import AdminResourceBaseView, AdminView


def create_blueprint(app):
    """Create blueprint."""
    endpoint = "administration"
    url = "/administration"
    menu_key = "admin_navigation"
    entry_point_group = "invenio_administration.views"

    blueprint = Blueprint(
        endpoint,
        __name__,
        url_prefix=url,
        template_folder="templates",
        static_folder="static",
    )

    admin_menu = AdminMenu(app)
    administration = Administration(
        menu=admin_menu,
        name=app.config["ADMINISTRATION_APPNAME"],
        base_template=app.config["ADMINISTRATION_BASE_TEMPLATE"],
        dashboard_config=app.config["ADMINISTRATION_DASHBOARD_VIEW"],
    )
    view_classes = []
    load_entry_point_group(administration, blueprint, entry_point_group, view_classes)

    with app.app_context():
        for view_class, extension_name in view_classes:
            if view_class.resource_config:
                view_class.set_resource(extension_name=extension_name)
            if view_class.schema:
                view_class.set_schema(extension_name=extension_name)

        admin_menu.register_menu_entries(menu, menu_key)
        admin_menu.register_admin_entry(menu, endpoint)

    return blueprint


def load_entry_point_group(administration, blueprint, entry_point_group, view_classes):
    """Load admin interface views from entry point group."""
    entrypoints = set(importlib_metadata.entry_points(group=entry_point_group))
    for ep in entrypoints:
        entry_point = _load_entry_point(ep)
        entrypoint_path = ep.value

        extension_name_from_path = _extract_extension_name(entrypoint_path)
        extension_name_from_view = entry_point.extension_name

        # fallback to extracted extension_name if property not set on view
        extension_name = extension_name_from_view or extension_name_from_path

        _register_view(
            entry_point,
            extension_name,
            administration,
            blueprint,
            view_classes,
        )


def _extract_extension_name(entrypoint_path):
    name = entrypoint_path.split(".")[0]
    return name.replace("_", "-")


def _load_entry_point(entry_point):
    """Load one entry point. Validates whether its view is an AdminView."""
    ep = entry_point.load()
    if not issubclass(ep, AdminView):
        msg = f"View class must be of type {AdminView.__name__}"
        raise TypeError(msg)
    return ep


def _register_view(view_class, extension_name, administration, blueprint, view_classes):
    """Register an admin view on this admin instance.

    :param view_class: The view class name passed to the view factory.
    :param extension_name: The name of the extension associated with the view.
    :param args: Positional arguments for view class.
    :param kwargs: Keyword arguments to view class.
    """
    view_instance = view_class(extension_name=extension_name, admin=administration)
    view = view_class.as_view(
        view_class.name,
        extension_name=extension_name,
        admin=administration,
    )
    administration.add_view(view, view_instance)
    blueprint.add_url_rule(rule=view_instance.url, view_func=view)
    if issubclass(view_class, AdminResourceBaseView):
        view_classes.append((view_class, extension_name))
