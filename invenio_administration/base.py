# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Administration views base module."""
from flask import current_app, render_template
from flask.views import MethodView
from flask_security import roles_required

from invenio_administration.errors import InvalidResource
from invenio_administration.marshmallow_utils import jsonify_schema


class AdminBaseView(MethodView):
    """Base view for admin views."""

    _extension = None
    name = None
    category = None
    endpoint = None
    template = "invenio_administration/index.html"
    url = None

    decorators = [roles_required("admin")]

    def __init__(
        self,
        name=__name__,
        category=None,
        endpoint=None,
        url=None,
        extension=None,
        admin=None,
    ):
        """Constructor."""
        if self._extension is None:
            self._extension = extension

        if self.name is None:
            self.name = name

        if self.category is None:
            self.category = category

        self.administration = admin

        self.endpoint = self._get_endpoint(endpoint)
        self.url = url or self._get_view_url(self.url)

        # Default view
        if self.get is None:
            raise Exception(
                "Cannot instantiate administration view"
                f" {self.__class__.__name__} "
                "without a default GET view"
            )

    def _get_view_extension(self):
        """Get the flask extension of the view."""
        return current_app.extensions[self._extension]

    @property
    def endpoint_location_name(self):
        """Get name for endpoint location e.g: 'administration.index'."""
        print(self.administration, "ADMIN-----")
        if self.administration is None:
            return self.endpoint
        return f"{self.administration.endpoint}.{self.endpoint}"

    def _get_endpoint(self, endpoint=None):
        """Generate Flask endpoint name.

        Defaults to class name if not provided.
        """
        if endpoint:
            return endpoint

        if not self.endpoint:
            return f"{self.name.lower()}"

    def _get_view_url(self, url):
        """Generate URL for the view. Override to change default behavior."""
        if url is None:
            if isinstance(self, self.administration.dashboard_view_class):
                url = "/"
            else:
                url = "/%s" % self.endpoint
        else:
            if not url.startswith("/"):
                url = "%s/%s" % (self.administration.url, url)

        return url

    def _get_template(self):
        return f"{self.template}"

    def render(self, **kwargs):
        """Render template."""
        kwargs["admin_base_template"] = self.administration.base_template
        return render_template(self._get_template(), **kwargs)

    def get(self):
        """GET view method."""
        return self.render()


class AdminResourceBaseView(AdminBaseView):
    """Base view for admin resources."""

    display_edit = False
    display_delete = False
    resource = None
    actions = {}
    schema = None

    def __init__(
        self,
        name=__name__,
        category=None,
        endpoint=None,
        url=None,
        extension=None,
        admin=None,
    ):
        """Constructor."""
        super().__init__(name, category, endpoint, url, extension, admin)

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

    def get(self, pid_value=None):
        """GET view method."""
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
        pass

    def get(self):
        """GET view method."""
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
