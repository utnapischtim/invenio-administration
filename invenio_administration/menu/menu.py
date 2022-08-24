# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Administration menu module."""

from flask import request


class AdminMenu:
    """Main class for the admin menu."""

    def __init__(self):
        """Constructor."""
        self._menu_items = []

    @property
    def items(self):
        """Return all raw menu items."""
        return self._menu_items

    def register_menu_entries(self, flask_menu_instance, menu_key="admin_navigation"):
        """Register all menu items to a flask menu instance."""
        main_menu = flask_menu_instance.submenu(menu_key)

        for menu_entry in self._menu_items:
            category = menu_entry.category
            name = menu_entry.name
            endpoint = menu_entry.endpoint
            order = menu_entry.order
            active_when = menu_entry.active_when
            if category:
                category_menu = main_menu.submenu(category)
                category_menu.register(text=category)
                category_menu.submenu(name).register(
                    endpoint=endpoint,
                    text=name,
                    order=order,
                    active_when=active_when or self.default_active_when,
                )
            else:
                main_menu.submenu(name).register(
                    endpoint=endpoint,
                    text=name,
                    order=order,
                    active_when=active_when or self.default_active_when,
                )

    def add_menu_item(self, item, index=None):
        """Add menu item."""
        if not isinstance(item, MenuItem):
            return TypeError("Item should be MenuItem instance.")

        if index:
            self._menu_items[index] = item
            return

        self._menu_items.append(item)

    def add_view_to_menu(self, view, index=None):
        """Add menu item from view."""
        menu_item = MenuItem(
            endpoint=view.endpoint_location_name,
            name=view.name,
            category=view.category,
        )
        self.add_menu_item(menu_item, index)

    @staticmethod
    def default_active_when(self):
        """Default condition for the menu item active state."""
        return request.endpoint == self._endpoint


class MenuItem:
    """Class for menu item."""

    def __init__(self, name="", endpoint="", category="", order=0, active_when=None):
        """Constructor."""
        self.name = name
        self.endpoint = endpoint
        self.category = category
        self.order = order
        self.active_when = active_when
