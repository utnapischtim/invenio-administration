/*
 * This file is part of Invenio.
 * Copyright (C) 2022 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */
import PropTypes from "prop-types";
import React, { Component } from "react";
import _get from "lodash/get";
import { Table } from "semantic-ui-react";

export class SearchResultItem extends Component {
  render() {
    const { result, columns } = this.props;

    return (
      <Table.Row>
        {columns.map(([property, { text, order }]) => {
          return (
            <Table.Cell key={`${text}-${order}`} data-label={text}>
              {_get(result, property)}
            </Table.Cell>
          );
        })}
      </Table.Row>
    );
  }
}

SearchResultItem.propTypes = {
  result: PropTypes.object.isRequired,
  columns: PropTypes.array.isRequired,
};
