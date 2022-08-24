# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Administration views base module."""
from functools import partial

from flask import current_app, render_template, url_for
from flask.views import MethodView
from flask_security import roles_required
from invenio_search_ui.searchconfig import search_app_config

from invenio_administration.errors import (
    InvalidExtensionName,
    InvalidResource,
    MissingDefaultGetView,
    MissingExtensionName,
    MissingResourceConfiguration,
)
from invenio_administration.marshmallow_utils import jsonify_schema

# class AdminViewType(MethodViewType):
#     """Metaclass for :class:`AdminView`."""
#
#     def __init__(cls, name, bases, d):
#         super().__init__(name, bases, d)
#         if "extension" in d:
#             cls._extension = d["extension"]
#


class AdminBaseView(MethodView):
    """Base view for admin views."""

    extension_name = None
    name = None
    category = None
    template = "invenio_administration/index.html"
    url = None
    menu_label = None

    decorators = [roles_required("admin")]

    def __init__(
        self,
        name=__name__,
        category=None,
        url=None,
        extension_name=None,
        admin=None,
    ):
        """Constructor."""
        if self.extension_name is None:
            self.extension_name = extension_name

        if self.name is None:
            self.name = name

        if self.category is None:
            self.category = category

        if self.menu_label is None:
            self.menu_label = self.name

        self.administration = admin

        self.url = url or self._get_view_url(self.url)

        # Default view
        if self.get is None:
            raise MissingDefaultGetView(self.__class__.__name__)

    @property
    def endpoint(self):
        """Get name for endpoint location e.g: 'administration.index'."""
        if self.administration is None:
            return self.name
        return f"{self.administration.endpoint}.{self.name}"

    @classmethod
    def _get_view_extension(cls, extension_name=None):
        """Get the flask extension of the view."""
        try:
            if extension_name:
                return current_app.extensions[extension_name]
            return current_app.extensions[cls.extension_name]
        except KeyError:
            raise InvalidExtensionName(extension_name)

    def _get_view_url(self, url):
        """Generate URL for the view. Override to change default behavior."""
        new_url = url
        if new_url is None:
            if isinstance(self, self.administration.dashboard_view_class):
                new_url = "/"
            else:
                new_url = "/%s" % self.name.lower()
        else:
            if not url.startswith("/"):
                new_url = "/%s" % (url)
        # Sanitize url
        new_url = new_url.replace(" ", "_")
        return new_url

    def _get_template(self):
        return self.template

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
    resource_config = None
    resource = None
    actions = {}
    schema = None

    def __init__(
        self,
        name=__name__,
        category=None,
        url=None,
        extension_name=None,
        admin=None,
    ):
        """Constructor."""
        super().__init__(name, category, url, extension_name, admin)

        if self.extension_name is None:
            raise MissingExtensionName(self.__class__.__name__)
        if self.resource_config is None:
            raise MissingResourceConfiguration(self.__class__.__name__)

    @classmethod
    def set_schema(cls):
        """Set schema."""
        cls.schema = cls._get_service_schema()

    @classmethod
    def set_resource(cls, extension_name=None):
        """Set resource."""
        cls.resource = cls._get_resource(extension_name)

    @classmethod
    def _get_resource(cls, extension_name=None):
        extension_name = cls._get_view_extension(extension_name)
        try:
            return getattr(extension_name, cls.resource_config)
        except AttributeError:
            raise InvalidResource(resource=cls.resource_config, view=cls.__name__)

    @classmethod
    def _get_service_schema(cls):
        # schema.schema due to the schema wrapper imposed,
        # when the actual class needed
        return cls.resource.service.schema.schema()

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
        serialized_schema = self._schema_to_json(schema)
        fields = self.item_field_list

        # TODO context processor?
        return self.render(
            ** {
                "resource_schema": serialized_schema,
                "fields": fields,
                "exclude_fields": self.item_field_exclude_list,
            }
        )


class AdminResourceListView(AdminResourceBaseView):
    """List view based on provided resource."""

    display_create = False

    # decides if there is a detail view
    display_read = True

    search_config_name = None
    search_facets_config_name = None
    search_sort_config_name = None
    sort_options = {}
    available_facets = {}
    item_field_exclude_list = None
    item_field_list = None
    template = "invenio_administration/search.html"
    api_endpoint = None
    list_title = None

    search_request_headers = {"Accept": "application/vnd.inveniordm.v1+json"}

    def get_search_request_headers(self):
        """Get search request headers."""
        return self.search_request_headers

    def get_search_app_name(self):
        """Get search app name."""
        if self.search_config_name is None:
            return f"{self.name.upper()}_SEARCH"
        return self.search_config_name

    def get_search_api_endpoint(self):
        """Get search API endpoint."""
        api_url_prefix = current_app.config["SITE_API_URL"]
        slash_tpl = "/" if not self.api_endpoint.startswith("/") else ""

        if not self.api_endpoint.startswith(api_url_prefix):
            return f"{api_url_prefix}{slash_tpl}{self.api_endpoint}"

        return f"{slash_tpl}{self.api_endpoint}"

    def init_search_config(self):
        """Build search view config."""
        return partial(
            search_app_config,
            config_name=self.get_search_app_name(),
            available_facets=current_app.config.get(self.search_facets_config_name),
            sort_options=current_app.config[self.search_sort_config_name],
            endpoint=self.get_search_api_endpoint(),
            headers=self.get_search_request_headers(),
        )

    def get_sort_options(self):
        """Get search sort options."""
        if not self.sort_options:
            return self.resource.service.config.search.sort_options
        return self.sort_options

    def get_available_facets(self):
        """Get search available facets."""
        if not self.available_facets:
            return self.resource.service.config.search.facets
        return self.available_facets

    def get(self):
        """GET view method."""
        search_conf = self.init_search_config()
        schema = self._get_service_schema()
        serialized_schema = self._schema_to_json(schema)
        return self.render(
            **{
                "search_config": search_conf,
                "list_title": self.list_title,
                "name": self.name,
                "resource_schema": serialized_schema,
                "fields": self.item_field_list,
            }
        )


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
