import React, { Component } from "react";
import PropTypes from "prop-types";
import { InvenioAdministrationActionsApi } from "../api/actions";
import { Grid, Loader } from "semantic-ui-react";

import { AdminForm } from "../formik/AdminForm";

export class EditPage extends Component {
  constructor(props) {
    super(props);
    this.state = { loading: true, resource: undefined };
  }

  componentDidMount() {
    this.getResource();
  }

  getResource = async () => {
    const { apiEndpoint, pid } = this.props;
    try {
      const response = await InvenioAdministrationActionsApi.getResource(
        apiEndpoint,
        pid
      );
      this.setState({
        loading: false,
        resource: response.data,
        // error: undefined,
      });
    } catch (e) {
      console.error(e);
      //TODO
    }
  };

  render() {
    const { resourceSchema, apiEndpoint, pid } = this.props;
    const { loading, resource } = this.state;

    if (loading) {
      return <Loader active={loading} />;
    }

    return (
      <Grid>
        <Grid.Column width={12}>
          <AdminForm
            resourceSchema={resourceSchema}
            resource={resource}
            apiEndpoint={apiEndpoint}
            pid={pid}
          />
        </Grid.Column>
      </Grid>
    );
  }
}

EditPage.propTypes = {
  resourceSchema: PropTypes.object.isRequired,
  apiEndpoint: PropTypes.string.isRequired,
  pid: PropTypes.string.isRequired,
};
