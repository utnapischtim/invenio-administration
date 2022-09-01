import React, { Component } from "react";
import PropTypes from "prop-types";
import { Delete } from "./Delete";

export class Actions extends Component {
  render() {
    const {
      displayEdit,
      displayDelete,
      actions,
      apiEndpoint,
      resource,
      successCallback,
      idKeyPath,
    } = this.props;

    // if number of actions is greater than 3, we display all in a dropdown
    // TODO remove this rule disabling when dropdown display is implemented.
    // eslint-disable-next-line no-unused-vars
    const displayAsDropdown =
      displayEdit && displayDelete && Object.keys(actions).length > 1;

    return (
      <Delete
        apiEndpoint={apiEndpoint}
        resource={resource}
        successCallback={successCallback}
        idKeyPath={idKeyPath}
      />
    );
  }
}

Actions.propTypes = {
  displayEdit: PropTypes.bool,
  displayDelete: PropTypes.bool,
  apiEndpoint: PropTypes.string,
  resource: PropTypes.object.isRequired,
  successCallback: PropTypes.func.isRequired,
  idKeyPath: PropTypes.string,
  actions: PropTypes.array.isRequired,
};

Actions.defaultProps = {
  displayEdit: true,
  displayDelete: true,
  apiEndpoint: undefined,
  idKeyPath: "pid",
};
