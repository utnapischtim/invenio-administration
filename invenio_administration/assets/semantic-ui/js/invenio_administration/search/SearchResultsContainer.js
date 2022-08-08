/*
 * This file is part of Invenio.
 * Copyright (C) 2022 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import PropTypes from "prop-types";
import React from "react";
import { Table } from "semantic-ui-react";

export const SearchResultsContainer = ({ results, columns }) => {
  return (
    <Table>
      <Table.Header>
        <Table.Row>
          {Object.keys(columns).map((key, index) => {
            return (
              <Table.HeaderCell key={`${key}-${index}`}>
                {columns[key]}
              </Table.HeaderCell>
            );
          })}
        </Table.Row>
      </Table.Header>
      <Table.Body>{results}</Table.Body>
    </Table>
  );
};

SearchResultsContainer.propTypes = {
  results: PropTypes.object.isRequired,
  columns: PropTypes.object.isRequired,
};
