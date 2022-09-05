import React, { Component } from "react";
import PropTypes from "prop-types";
import { Form, Formik } from "formik";
import { InvenioAdministrationActionsApi } from "../api/actions";
import { Button, Modal } from "semantic-ui-react";
import { Form as SemanticForm } from "semantic-ui-react";
import { Json2Formik } from "./utils";

export class ActionForm extends Component {
  constructor(props) {
    super(props);
    const { resource } = props;

    this.state = {
      loading: false,
      // error: undefined,
      formData: resource,
    };
  }

  onSubmit = async ({ formData }, e) => {
    this.setState({ loading: true });
    const { actionKey, actionSuccessCallback } = this.props;
    const actionEndpoint = this.getEndpoint(actionKey);

    try {
      const response = InvenioAdministrationActionsApi.resourceAction(
        actionEndpoint,
        formData
      );
      this.setState({ loading: false });
      actionSuccessCallback(response.data);
    } catch (e) {
      console.error(e);
      //TODO
    }
  };

  onCancel = () => {
    const { resource, actionCancelCallback } = this.props;
    this.setState({ formData: resource });
    actionCancelCallback();
  };

  getEndpoint = (actionKey) => {
    const { resource } = this.props;
    // get the action endpoint from the current resource links
    return resource.links.actions[actionKey];
  };

  render() {
    const { actionSchema } = this.props;
    const { loading, formData } = this.state;
    return (
      <Formik initialValues={formData} onSubmit={this.onSubmit}>
        {(props) => (
          <SemanticForm as={Form} onSubmit={props.handleSubmit}>
            <Json2Formik jsonSchema={actionSchema} formikProps={props} />
            <Modal.Actions>
              <Button type="button" onClick={this.onCancel}>
                Cancel
              </Button>
              <Button type="submit" primary loading={loading}>
                Save
              </Button>
            </Modal.Actions>
          </SemanticForm>
        )}
      </Formik>
    );
  }
}

ActionForm.propTypes = {
  resource: PropTypes.object.isRequired,
  actionSchema: PropTypes.object.isRequired,
  actionKey: PropTypes.string.isRequired,
  actionSuccessCallback: PropTypes.func.isRequired,
  actionCancelCallback: PropTypes.func.isRequired,
};
