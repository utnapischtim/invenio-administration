# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Administration dashboard view."""

from invenio_administration.base import AdminBaseView
from invenio_administration.decorators import expose


class AdminDashboardView(AdminBaseView):
    """Default view for the ``/admin/`` URL.

    It can be overridden,
    by passing your own view class to the ``Admin`` constructor::

        class MyHomeView(AdminDashboardView):
            @expose('/')
            def index(self):
                arg1 = 'Hello'
                return self.render('myadmin/myhome.html', arg1=arg1)
        admin = Admin(dashboard_view=MyHomeView())
    Also, you can change the root url from /admin to / with the following::
        admin = Admin(
            app,
            dashboard_view=AdminDashboardView(
                name='Home',
                template='invenio_admin/myhome.html',
                url='/'
            )
        )
    Default values for the index page are:
    * If a name is not provided, 'Home' will be used.
    * If an endpoint is not provided, will default to ``admin``
    * Default URL route is ``/admin``.
    * Default template is ``invenio_admin/index.html``
    """

    def __init__(
        self,
        name=None,
        category=None,
        endpoint=None,
        url=None,
        template="invenio_administration/index.html",
    ):
        """Constructor."""
        super(AdminDashboardView, self).__init__(
            name or "Home",
            category,
            endpoint or "administration",
            "/administration" if url is None else url,
        )
        self.template = template

    @expose()
    def index(self):
        """Main view."""
        return self.render()
