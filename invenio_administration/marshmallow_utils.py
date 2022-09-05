# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio administration marshmallow utils module."""

from invenio_vocabularies.services.schema import VocabularySchema
from marshmallow import fields
from marshmallow_utils import fields as invenio_fields


def jsonify_schema(schema):
    """Marshmallow schema to dict."""
    schema_dict = {}

    custom_mapping = {
        # marshmallow
        fields.Str: "string",
        fields.Integer: "integer",
        fields.List: "array",
        fields.Dict: "object",
        fields.Url: "string",
        fields.String: "string",
        fields.DateTime: "datetime",
        fields.Float: "float",
        fields.Boolean: "bool",
        fields.Raw: "dict",
        fields.UUID: "uuid",
        fields.Time: "time",
        fields.Date: "date",
        fields.TimeDelta: "timedelta",
        fields.Decimal: "decimal",
        # invenio fields
        invenio_fields.SanitizedUnicode: "string",
        invenio_fields.links.Links: "array",
        invenio_fields.links.Link: "string",
        invenio_fields.tzdatetime.TZDateTime: "string",
        invenio_fields.sanitizedhtml.SanitizedHTML: "string",
    }
    for field, field_type in schema.fields.items():
        is_read_only = field_type.dump_only
        is_create_only = field_type.metadata["create_only"] \
            if "create_only" in field_type.metadata else False

        field_type_name = field_type.__class__
        is_required = field_type.required

        nested_field = isinstance(field_type, fields.Nested)
        list_field = isinstance(field_type, fields.List)

        if nested_field:
            if isinstance(field_type.schema, VocabularySchema):
                schema_type = "vocabulary"
            else:
                schema_type = "object"

            schema_dict[field] = {
                "type": schema_type,
                "title": field_type.metadata[
                    "title"] if "title" in field_type.metadata else None,
                "required": is_required,
                "properties": jsonify_schema(field_type.schema),
                "readOnly": is_read_only,
                "createOnly": is_create_only
            }
        elif list_field and hasattr(field_type, "properties"):
            schema_dict[field] = {
                "type": "array",
                "properties": jsonify_schema(field_type.inner.schema),
                "required": is_required,
                "readOnly": is_read_only,
                "createOnly": is_create_only,
                "title": field_type.metadata[
                    "title"] if "title" in field_type.metadata else None,
            }

        else:
            try:
                schema_dict[field] = {
                    "type": custom_mapping[field_type_name],
                    "required": is_required,
                    "readOnly": is_read_only,
                    "createOnly": is_create_only,
                    "title": field_type.metadata[
                        "title"] if "title" in field_type.metadata else None
                }
            except KeyError:
                raise Exception(f"Unrecognised schema field {field}: {field_type_name}")

    json_schema = {"$schema": "http://json-schema.org/draft-07/schema#",
                   "properties": schema_dict,
                   }
    return json_schema
