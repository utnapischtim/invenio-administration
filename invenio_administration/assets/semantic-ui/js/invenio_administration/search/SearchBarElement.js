/*
 * This file is part of Invenio.
 * Copyright (C) 2022 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import React, { Component } from "react";
import { withState } from "react-searchkit";
import { Input } from "semantic-ui-react";
import PropTypes from "prop-types";

export class SearchBarComponent extends Component {
  constructor(props) {
    super(props);

    const { queryString } = props;

    this.state = {
      currentQuery: queryString || "",
    };
  }

  onInputChange = (e, { value }) => {
    this.setState({
      currentQuery: value,
    });
  };

  search = (query) => {
    const { updateQueryState, currentQueryState } = this.props;
    updateQueryState({ ...currentQueryState, queryString: query });
  };

  onBtnSearchClick = () => {
    const { currentQuery } = this.state;
    this.search(currentQuery);
  };

  onKeyPress = (event) => {
    if (event.key === "Enter") {
      const { currentQuery } = this.state;
      this.search(currentQuery);
    }
  };

  render() {
    const { placeholder, queryString, uiProps } = this.props;

    return (
      <Input
        action={{
          icon: "search",
          onClick: this.onBtnSearchClick,
          className: "search",
        }}
        fluid
        placeholder={placeholder}
        onChange={this.onInputChange}
        value={queryString}
        onKeyPress={this.onKeyPress}
        {...uiProps}
      />
    );
  }
}

SearchBarComponent.propTypes = {
  queryString: PropTypes.string.isRequired,
  updateQueryState: PropTypes.func.isRequired,
  currentQueryState: PropTypes.object.isRequired,
  placeholder: PropTypes.string.isRequired,
  uiProps: PropTypes.object,
};

SearchBarComponent.defaultProps = {
  uiProps: undefined,
};

export const SearchBar = withState(SearchBarComponent);
