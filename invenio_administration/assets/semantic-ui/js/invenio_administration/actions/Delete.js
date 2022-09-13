import React, { Component } from "react";
import PropTypes from "prop-types";
import { Button, Icon } from "semantic-ui-react";
import { InvenioAdministrationActionsApi } from "../api/actions";

export class Delete extends Component {
  constructor(props) {
    super(props);
    this.state = { loading: false };
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
    const { Element } = this.props;
    return (
      <Element
        icon
        negative
        onClick={this.handleOnButtonClick}
        loading={loading}
      >
        <Icon name="trash alternate" />
      </Element>
    );
  }
}

Delete.propTypes = {
  apiEndpoint: PropTypes.string.isRequired,
  resource: PropTypes.object.isRequired,
  successCallback: PropTypes.func.isRequired,
  Element: PropTypes.object,
  idKeyPath: PropTypes.string.isRequired,
};

Delete.defaultProps = {
  Element: Button,
};
