# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Administration exceptions."""

from flask_babelex import gettext as _


class InvalidResource(Exception):
    """Exception for invalid resources."""

    def __init__(self, resource, view):
        """Initialise error."""
        super().__init__(_(f"Invalid resource {resource} configured for view {view}."))


class InvalidExtensionName(KeyError):
    """Exception for invalid extension names."""

    def __init__(self, extension_name):
        """Initialise error."""
        super().__init__(_(f"No extension found with name '{extension_name}' ."))


class MissingResourceConfiguration(Exception):
    """Exception for missing resource configurations."""

    def __init__(self, name):
        """Initialise error."""
        super().__init__(
            f"Cannot instantiate resource view {name} "
            f"without a resource."
        )


class MissingExtensionName(Exception):
    """Exception for missing resource configurations."""

    def __init__(self, name):
        """Initialise error."""
        super().__init__(
            f"Cannot instantiate resource view {name} "
            f"without an associated flask extension."
        )


class MissingDefaultGetView(Exception):
    """Exception for missing default GET views."""

    def __init__(self, name):
        """Initialise error."""
        super().__init__(
            "Cannot instantiate administration view"
            f" {name} "
            "without a default GET view"
        )
