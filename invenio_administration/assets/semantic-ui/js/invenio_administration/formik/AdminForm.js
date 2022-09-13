import React, { Component } from "react";
import PropTypes from "prop-types";
import { Form, Formik } from "formik";
import { Form as SemanticForm, Loader } from "semantic-ui-react";
import { InvenioAdministrationActionsApi } from "../api/actions";
import { Button } from "semantic-ui-react";
import { GenerateForm } from "./GenerateForm";

export class AdminForm extends Component {
  constructor(props) {
    super(props);
    const { resource } = props;

    this.state = {
      loading: false,
      // error: undefined,
      formData: resource,
    };
  }

  onSubmit = async (values) => {
    const { apiEndpoint, pid } = this.props;
    this.setState({ loading: true });
    try {
      await InvenioAdministrationActionsApi.editResource(
        apiEndpoint,
        pid,
        values
      );
      this.setState({ loading: false });
    } catch (e) {
      console.error(e);
      //TODO
    }
  };

  onCancel = () => {
    const { resource } = this.props;
    this.setState({ formData: resource });
  };

  render() {
    const { resourceSchema, create, formFields } = this.props;
    const { formData, loading } = this.state;
    if (loading) {
      return <Loader active={loading} />;
    }

    return (
      <Formik initialValues={formData} onSubmit={this.onSubmit}>
        {(props) => (
          <SemanticForm as={Form} onSubmit={props.handleSubmit}>
            <GenerateForm
              formFields={formFields}
              jsonSchema={resourceSchema}
              create={create}
            />
            <Button type="button" onClick={this.onCancel} loading={loading}>
              Cancel
            </Button>
            <Button type="submit" primary loading={loading}>
              Save
            </Button>
          </SemanticForm>
        )}
      </Formik>
    );
  }
}

AdminForm.propTypes = {
  resource: PropTypes.object,
  resourceSchema: PropTypes.object.isRequired,
  apiEndpoint: PropTypes.string.isRequired,
  pid: PropTypes.string,
  create: PropTypes.bool,
  formFields: PropTypes.object,
};

AdminForm.defaultProps = {
  resource: undefined,
  create: false,
  pid: undefined,
  formFields: undefined,
};
