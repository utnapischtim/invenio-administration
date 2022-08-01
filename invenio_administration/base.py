# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Administration views base module."""

from flask import Blueprint, abort, current_app, render_template, url_for

from invenio_administration.decorators import _wrap_view, expose
from invenio_administration.errors import InvalidResource
from invenio_administration.marshmallow_utils import jsonify_schema


class AdminViewMeta(type):
    """View metaclass.

    Does pre-calculations (like getting list of view methods from the class)
    to avoid calculating them for each view class instance.
    """

    def __init__(cls, classname, bases, fields):
        """Constructor."""
        type.__init__(cls, classname, bases, fields)

        # Gather exposed views
        cls._urls = []
        cls._default_view = None
        for p in dir(cls):
            attr = getattr(cls, p)
            # import ipdb;ipdb.set_trace()
            if hasattr(attr, "_urls"):
                # Collect methods
                for url, methods in attr._urls:
                    cls._urls.append((url, p, methods))

                    if url == "/":
                        # adds the default view automatically
                        cls._default_view = p

                # Wrap views
                setattr(cls, p, _wrap_view(attr))


class AdminBaseView(metaclass=AdminViewMeta):
    """Base view for admin views."""

    _extension = None
    name = None
    category = None
    endpoint = None
    template = "TODO"

    def __init__(
        self,
        name=__name__, category=None, endpoint=None, url=None, extension=None
    ):
        """Constructor."""
        if self._extension is None:
            self._extension = extension
        if self.name is None:
            self.name = name

        if self.category is None:
            self.category = category

        self.endpoint = self._get_endpoint(endpoint)
        self.url = url

        self.blueprint = None
        self.administration = None

        # Default view
        if self._default_view is None:
            raise Exception(
                "Cannot instantiate administration view"
                f" {self.__class__.__name__} "
                "without a default view"
            )

    def _get_view_extension(self):
        """Get the flask extension of the view."""
        return current_app.extensions[self._extension]

    @property
    def endpoint_location_name(self):
        """Get name for endpoint location e.g: 'administration.index'."""
        path, name, methods = self._urls[0]
        prefix = self.endpoint
        endpoint_name = prefix + "." + name
        return endpoint_name

    def _get_endpoint(self, endpoint=None):
        """Generate Flask endpoint name.

        Defaults to class name if not provided.
        """
        if endpoint:
            return endpoint

        if not self.endpoint:
            return self.name.lower()

    def _get_view_url(self, admin, url):
        """Generate URL for the view. Override to change default behavior."""
        if url is None:
            if admin.url != "/":
                url = "%s/%s" % (admin.url, self.endpoint)
            else:
                if self == admin.dashboard_view:
                    url = "/"
                else:
                    url = "/%s" % self.endpoint
        else:
            if not url.startswith("/"):
                url = "%s/%s" % (admin.url, url)

        return url

    def create_blueprint(self, admin):
        """Create Flask blueprint."""
        # Store admin instance
        self.administration = admin

        # Generate URL
        self.url = self._get_view_url(admin, self.url)

        # If we're working from the root of the site, set prefix to None
        if self.url == "/":
            self.url = None

        # Create blueprint and register rules
        self.blueprint = Blueprint(
            self.endpoint,
            __name__,
            url_prefix=self.url,
            template_folder="templates",
            static_folder="static",
        )

        for url, name, methods in self._urls:
            self.blueprint.add_url_rule(
                url, name, getattr(self, name), methods=methods
            )

        return self.blueprint

    def render(self, **kwargs):
        """Render template.

        :param template:
            Template path to render
        :param kwargs:
            Template arguments
        """
        kwargs["admin_base_template"] = self.administration.base_template

        return render_template(self.template, **kwargs)

    def _run_view(self, fn, *args, **kwargs):
        """This method will run actual view function.

        While it is similar to _handle_view, can be used to change
        arguments that are passed to the view.

        :param fn:
            View function
        :param kwargs:
            Arguments
        """
        return fn(self, *args, **kwargs)

    def is_accessible(self):
        """Override this method to add permission checks.

        Flask-Admin does not make assumptions about the authentication system
        used in your application, so it is up to you to implement it.
        By default, it will allow access for everyone.
        """
        return True

    def inaccessible_callback(self, name, **kwargs):
        """Handle the response to inaccessible views.

        By default, it throw HTTP 403 error. Override this method to
        customize the behaviour.
        """
        return abort(403)

    def _handle_view(self, name, **kwargs):
        """This method will be executed before calling any view method.

        It will execute the ``inaccessible_callback`` if the view is not
        accessible.
        :param name:
            View function name
        :param kwargs:
            View function arguments
        """
        if not self.is_accessible():
            return self.inaccessible_callback(name, **kwargs)


class AdminResourceBaseView(AdminBaseView):
    """Base view for admin resources."""

    display_edit = False
    display_delete = False
    resource = None
    actions = {}
    schema = None

    def __init__(
        self,
        name=__name__, category=None, endpoint=None, url=None, extension=None
    ):
        """Constructor."""
        super().__init__(name, category, endpoint, url, extension)

        if self._extension is None:
            raise Exception(
                f"Cannot instanciate resource view {self.__class__.__name__} "
                f"without an associated flask extension."
            )
        if self.resource is None:
            raise Exception(
                f"Cannot instanciate resource view {self.__class__.__name__} "
                f"without a resource."
            )

    def set_schema(self):
        """Set schema."""
        self.schema = self._get_service_schema()

    def _get_resource(self, extension):
        try:
            return getattr(extension, self.resource)
        except AttributeError:
            raise InvalidResource(resource=self.resource, view=self.name)

    def _get_service_schema(self):
        current_extension = self._get_view_extension()
        resource = self._get_resource(current_extension)
        # schema.schema due to the schema wrapper imposed,
        # when the actual class needed
        return resource.service.schema.schema()

    def _schema_to_json(self, schema):
        return jsonify_schema(schema)

    def serialize_actions(self):
        """Serialize actions for the resource view.

        {"action_name":
        {"text": "BLA"
         #"api_endpoint": either from links.actions or provided by the resource

         If provided by resource,
         there will be no mapping on the frontend side.

         Also means we don't have links generated with permissions.
         Best to have a specialized component,
         which knows from where to read the endpoint.

         "payload_schema": schema in json

        """


class AdminResourceDetailView(AdminResourceBaseView):
    """Details view based on given config."""

    item_field_exclude_list = None
    item_field_list = None
    template = "invenio_administration/details.html"

    @expose(url="/<pid_value:pid_value>")
    def index(self, pid_value=None):
        """Main details view."""
        schema = self._get_service_schema()
        serialize_schema = self._schema_to_json(schema)

        # TODO context processor?
        return self.render(**{"schema": serialize_schema})


class AdminResourceListView(AdminResourceBaseView):
    """List view based on provided resource."""

    display_create = False

    # decides if there is a detail view
    display_read = True

    sort_options = None
    available_filters = None
    column_exclude_list = None
    column_list = None
    template = "invenio_administration/search.html"

    def init_search_config(self):
        """Build search view config."""
        # TODO
        pass

    @expose()
    def index(self):
        """Main list view."""
        search_conf = self.init_search_config()
        schema = self._get_service_schema()
        return self.render(**{"search_config": search_conf})


class AdminResourceViewSet:
    """View set based on resource.

    Provides a list view and a details view given the provided configuration.
    """

    resource = None
    display_create = False

    # decides if there is a detail view
    display_read = True
    display_edit = False
    display_delete = False

    actions = None

    sort_options = ()
    available_filters = None
    column_exclude_list = None
    column_list = None

    item_field_exclude_list = None
    item_field_list = None

    list_view = None
    details_view = None

    def list_view(self):
        """List view."""
        pass

    def details_view(self):
        """Details view."""
        pass
