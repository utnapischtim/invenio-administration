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
        fields.Integer: "int",
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
        if field_type.dump_only:
            continue

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
                "required": is_required,
                "properties": jsonify_schema(field_type.schema),
            }
        elif list_field and hasattr(field_type, "properties"):
            schema_dict[field] = {
                "type": "array",
                "properties": jsonify_schema(field_type.inner.schema),
                "required": is_required,
            }

        else:
            try:
                schema_dict[field] = {
                    "type": custom_mapping[field_type_name],
                    "required": is_required,
                }
            except KeyError:
                raise Exception(
                    f"Unrecognised schema field {field}: {field_type_name}"
                )

    return schema_dict
