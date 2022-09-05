import React from "react";
import { Input } from "react-invenio-forms";
import _capitalize from "lodash/capitalize";
import PropTypes from "prop-types";

const fieldsMap = {
  string: Input,
  integer: Input,
  uuid: Input,
  datetime: Input,
};

const objMap = (obj, parentField, isCreate) => {
  const elements = Object.entries(obj).map(([fieldName, fieldSchema]) => {
    let currentFieldName;

    if (parentField) {
      currentFieldName = `${parentField}.${fieldName}`;
    } else {
      currentFieldName = fieldName;
    }

    if (fieldSchema.type === "array") {
      // TODO
    }

    if (fieldSchema.type === "object") {
      return objMap(fieldSchema.properties, currentFieldName);
    }

    const Element = fieldsMap[fieldSchema.type];

    return (
      <Element
        fieldPath={currentFieldName}
        key={currentFieldName}
        required={fieldSchema.required}
        disabled={fieldSchema.readOnly || (fieldSchema.createOnly && !isCreate)}
        label={
          fieldSchema.title
            ? _capitalize(fieldSchema.title)
            : _capitalize(fieldName)
        }
      />
    );
  });
  return elements;
};

export const Json2Formik = ({ jsonSchema, create }) => {
  const properties = jsonSchema.properties;
  return <>{objMap(properties, undefined, create)}</>;
};

Json2Formik.propTypes = {
  jsonSchema: PropTypes.object.isRequired,
  create: PropTypes.bool,
};

Json2Formik.defaultProps = {
  create: false,
};
