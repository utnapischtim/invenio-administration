import React, { Component } from "react";
import PropTypes from "prop-types";
import { Button, Icon } from "semantic-ui-react";
import { InvenioAdministrationActionsApi } from "../api/actions";

export class Delete extends Component {
  constructor(props) {
    super(props);
    // TODO remove this rule when error is implemented.
    // eslint-disable-next-line react/no-unused-state
    this.state = { loading: false, error: undefined };
  }

  handleOnButtonClick = async () => {
    const { successCallback, resource, apiEndpoint, idKeyPath } = this.props;
    try {
      await InvenioAdministrationActionsApi.deleteResource(
        resource,
        apiEndpoint,
        idKeyPath
      );
      successCallback();
    } catch (e) {
      // TODO
    }
  };

  render() {
    const { loading } = this.state;
    return (
      <Button
        labelPosition="left"
        icon
        negative
        onClick={this.handleOnButtonClick}
        loading={loading}
      >
        <Icon name="trash alternate" />
        Delete
      </Button>
    );
  }
}

Delete.propTypes = {
  apiEndpoint: PropTypes.string.isRequired,
  resource: PropTypes.object.isRequired,
  successCallback: PropTypes.func.isRequired,
  idKeyPath: PropTypes.string.isRequired,
};
