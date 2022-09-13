import React, { Component } from "react";
import PropTypes from "prop-types";
import { Delete } from "./Delete";
import isEmpty from "lodash/isEmpty";
import { ResourceActions } from "./ResourceActions";
import { ActionsDropdown } from "./ActionsDropdown";
import { Button, Icon } from "semantic-ui-react";
import { AdminUIRoutes } from "../routes";

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
      listUIEndpoint,
    } = this.props;

    // if number of actions is greater than 3, we display all in a dropdown
    const displayAsDropdown =
      displayEdit && displayDelete && Object.keys(actions).length > 1;

    if (displayAsDropdown) {
      return (
        <ActionsDropdown
          apiEndpoint={apiEndpoint}
          resource={resource}
          successCallback={successCallback}
          idKeyPath={idKeyPath}
          actions={actions}
          displayEdit={displayEdit}
          displayDelete={displayDelete}
        />
      );
    } else {
      return (
        <Button.Group size="tiny" className="relaxed">
          {!isEmpty(actions) && (
            <ResourceActions
              resource={resource}
              successCallback={successCallback}
              idKeyPath={idKeyPath}
              actions={actions}
              apiEndpoint={apiEndpoint}
            />
          )}
          {displayEdit && (
            <Button
              as="a"
              href={AdminUIRoutes.editView(listUIEndpoint, resource, idKeyPath)}
              icon
              labelPosition="left"
            >
              <Icon name="pencil" />
              Edit
            </Button>
          )}
          {displayDelete && (
            <Delete
              apiEndpoint={apiEndpoint}
              resource={resource}
              successCallback={successCallback}
              idKeyPath={idKeyPath}
            />
          )}
        </Button.Group>
      );
    }
  }
}

Actions.propTypes = {
  displayEdit: PropTypes.bool,
  displayDelete: PropTypes.bool,
  apiEndpoint: PropTypes.string,
  resource: PropTypes.object.isRequired,
  successCallback: PropTypes.func.isRequired,
  idKeyPath: PropTypes.string,
  actions: PropTypes.object.isRequired,
  listUIEndpoint: PropTypes.string.isRequired,
};

Actions.defaultProps = {
  displayEdit: true,
  displayDelete: true,
  apiEndpoint: undefined,
  idKeyPath: "pid",
};
