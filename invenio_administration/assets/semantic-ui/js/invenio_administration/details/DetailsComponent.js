// This file is part of InvenioAdministration
// Copyright (C) 2022 CERN.
//
// Invenio RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import PropTypes from "prop-types";
import React, { Component } from "react";
import Overridable from "react-overridable";
import { Table } from "semantic-ui-react";

class DetailsTable extends Component {
  generateTableRow(key, pair) {
    return (
      <Table.Row key={key}>
        <Table.Cell>
          <b>{key}</b>
        </Table.Cell>
        <Table.Cell>{pair}</Table.Cell>
      </Table.Row>
    );
  }

  render() {
    const { columns, data } = this.props;

    const tableRows = columns.map((col) => {
      const { key, text } = col;
      let value = data[key];

      if (text && value && typeof value === "object") {
        // TODO use formatters
      }

      if (text && value) {
        return this.generateTableRow(text, value);
      }
    });

    return (
      <Overridable id="DetailsComponent.table">
        <Table unstackable>
          <Table.Body>{tableRows}</Table.Body>
        </Table>
      </Overridable>
    );
  }
}

DetailsTable.propTypes = {
  data: PropTypes.object.isRequired,
  columns: PropTypes.array.isRequired,
};

export default Overridable.component("DetailsTable", DetailsTable);
