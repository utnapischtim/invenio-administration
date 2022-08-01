# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Configuration for Invenio-Admin."""

ADMINISTRATION_BASE_TEMPLATE = None
"""Admin panel base template.
By default (``None``) uses the Flask-Admin template."""

ADMINISTRATION_APPNAME = "Invenio-Administration"
"""Name of the Flask-Admin app (also the page title of admin panel)."""

# ADMINISTRATION_LOGIN_ENDPOINT = "security.login"
"""Endpoint name of the login view. Anonymous users trying to access admin
panel will be redirected to this endpoint."""

# ADMINISTRATION_LOGOUT_ENDPOINT = "security.logout"
"""Endpoint name of logout view."""

# ADMINISTRATION_PERMISSION_FACTORY =
# "invenio_administration.permissions.admin_permission_factory"
"""Permission factory for the admin views."""
