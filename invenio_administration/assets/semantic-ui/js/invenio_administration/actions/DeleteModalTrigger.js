// This file is part of InvenioAdministration
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { Component } from "react";
import PropTypes from "prop-types";
import { Button, Icon } from "semantic-ui-react";
import { DeleteModal } from "./DeleteModal";
import { Modal } from "semantic-ui-react";
import { Trans } from "react-i18next";

export class DeleteModalTrigger extends Component {
  constructor(props) {
    super(props);
    this.state = { modalOpen: false };
  }

  toggleModal = (open) => {
    this.setState({ modalOpen: open });
  };

  render() {
    const {
      title,
      resourceName,
      apiEndpoint,
      resource,
      successCallback,
      idKeyPath,
      Element,
    } = this.props;
    const { modalOpen } = this.state;
    return (
      <>
        <Element icon negative onClick={() => this.toggleModal(true)}>
          <Icon name="trash alternate" />
        </Element>
        <DeleteModal
          title={title}
          apiEndpoint={apiEndpoint}
          resource={resource}
          successCallback={successCallback}
          idKeyPath={idKeyPath}
          toggleModal={this.toggleModal}
          modalOpen={modalOpen}
        >
          <Modal.Content>
            <Modal.Description>
              <Trans
                defaults="Are you sure you want to delete {{resourceName}}? "
                values={{ resourceName: resource[resourceName] }}
              />
            </Modal.Description>
          </Modal.Content>
        </DeleteModal>
      </>
    );
  }
}

DeleteModalTrigger.propTypes = {
  title: PropTypes.string.isRequired,
  resourceName: PropTypes.string.isRequired,
  apiEndpoint: PropTypes.string.isRequired,
  resource: PropTypes.object.isRequired,
  successCallback: PropTypes.func.isRequired,
  Element: PropTypes.object,
  idKeyPath: PropTypes.string.isRequired,
};

DeleteModalTrigger.defaultProps = {
  Element: Button,
};
