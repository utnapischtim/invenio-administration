# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Administration decorators."""

from functools import wraps


def _wrap_view(f):
    # Avoid wrapping view method twice
    if hasattr(f, "_wrapped"):
        return f

    @wraps(f)
    def inner(self, *args, **kwargs):

        # Check if administrative piece is accessible
        abort = self._handle_view(f.__name__, **kwargs)
        if abort is not None:
            return abort

        return self._run_view(f, *args, **kwargs)

    inner._wrapped = True

    return inner


def expose(url="/", methods=("GET",)):
    """Use this decorator to expose views in your view classes.

    :param url:
        Relative URL for the view.
    :param methods:
        Allowed HTTP methods. By default only GET is allowed.
    """

    def wrap(f):
        if not hasattr(f, "_urls"):
            f._urls = []
        f._urls.append((url, methods))
        return f

    return wrap
