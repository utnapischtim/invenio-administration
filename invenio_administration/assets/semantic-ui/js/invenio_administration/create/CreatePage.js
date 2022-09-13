import React, { Component } from "react";
import PropTypes from "prop-types";
import { Grid, Loader } from "semantic-ui-react";
import { AdminForm } from "../formik/AdminForm";

export class CreatePage extends Component {
  constructor(props) {
    super(props);
    this.state = { loading: false };
  }

  render() {
    const { resourceSchema, apiEndpoint, formFields } = this.props;
    const { loading } = this.state;

    if (loading) {
      return <Loader active={loading} />;
    }

    return (
      <Grid>
        <Grid.Column width={12}>
          <AdminForm
            resourceSchema={resourceSchema}
            apiEndpoint={apiEndpoint}
            formFields={formFields}
            create
          />
        </Grid.Column>
      </Grid>
    );
  }
}

CreatePage.propTypes = {
  resourceSchema: PropTypes.object.isRequired,
  apiEndpoint: PropTypes.string.isRequired,
  formFields: PropTypes.object,
};

CreatePage.defaultProps = {
  formFields: undefined,
};
