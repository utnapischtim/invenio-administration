# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Administration menu test module."""

from invenio_administration.dashboard import AdminDashboardView


def test_menu_generation(
    current_admin_menu,
    current_admin_app,
    current_admin_ext,
    current_app
):
    name = "Test name"
    category = "Test category"
    endpoint = "test_endpoint"
    url = "test_url"
    # test view so that we can test its properties
    test_view = AdminDashboardView(
        name=name,
        category=category,
        endpoint=endpoint,
        url=url
    )

    # register the view equal to the above one and add it to app
    current_admin_ext.register_view(
        AdminDashboardView,
        name=name,
        category=category,
        endpoint=endpoint,
        url=url
    )

    # register menu items on flask-menu instance
    current_admin_app._menu.register_menu_entries(current_admin_menu)
    # default admin navigation menu
    flask_menu_admin_instance = \
        current_admin_menu.submenu("admin_navigation")

    # check if menu category was made correctly and has children
    category_menu = flask_menu_admin_instance.submenu(category)
    assert category_menu.text == category
    assert len(category_menu.children) > 0
    # menu entry from the registered view
    menu_entry = category_menu.children[0]

    # check if correct menu entry made under the category
    assert menu_entry.text == name
    assert menu_entry._endpoint == test_view.endpoint_location_name

    # needs context to generate url from endpoint
    app_context = current_app.app_context()
    test_context = current_app.test_request_context()
    with app_context, test_context:
        expected_url = f"/administration/{url}/"
        # check if url from endpoint matches expected url
        assert menu_entry.url == expected_url
