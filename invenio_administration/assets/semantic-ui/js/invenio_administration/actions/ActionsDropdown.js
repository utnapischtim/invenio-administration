import React, { Component } from "react";
import PropTypes from "prop-types";
import { Dropdown } from "semantic-ui-react";
import { Delete } from "./Delete";
import { ResourceActions } from "./ResourceActions";
import isEmpty from "lodash/isEmpty";

export class ActionsDropdown extends Component {
  render() {
    const {
      displayEdit,
      displayDelete,
      apiEndpoint,
      resource,
      successCallback,
      idKeyPath,
      actions,
    } = this.props;
    return (
      <Dropdown>
        {!isEmpty(actions) && (
          <ResourceActions
            resource={resource}
            successCallback={successCallback}
            idKeyPath={idKeyPath}
            actions={actions}
            apiEndpoint={apiEndpoint}
            Element={Dropdown.Item}
          />
        )}
        {displayEdit && <Dropdown.Item>Edit</Dropdown.Item>}
        {displayDelete && (
          <Delete
            apiEndpoint={apiEndpoint}
            resource={resource}
            successCallback={successCallback}
            idKeyPath={idKeyPath}
            Element={Dropdown.Item}
          />
        )}
      </Dropdown>
    );
  }
}

ActionsDropdown.propTypes = {
  displayEdit: PropTypes.bool,
  displayDelete: PropTypes.bool,
  apiEndpoint: PropTypes.string.isRequired,
  resource: PropTypes.object.isRequired,
  successCallback: PropTypes.func.isRequired,
  idKeyPath: PropTypes.string.isRequired,
  actions: PropTypes.object.isRequired,
};

ActionsDropdown.defaultProps = {
  displayDelete: true,
  displayEdit: true,
};
