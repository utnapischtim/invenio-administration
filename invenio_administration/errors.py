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
        super().__init__(
            _(
                f"Invalid resource {resource} configured for view {view}."
            )
        )
