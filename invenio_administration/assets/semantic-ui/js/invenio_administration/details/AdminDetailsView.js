import PropTypes from "prop-types";
import React, { Component } from "react";
import { Grid, Header, Segment, Dimmer, Loader } from "semantic-ui-react";
import { InvenioAdministrationActionsApi } from "../api/actions";
import DetailsTable from "./DetailsComponent";
import { Actions } from "../actions/Actions";
import _isEmpty from "lodash/isEmpty";
import { ErrorPage } from "../components/ErrorPage";

export default class AdminDetailsView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      data: undefined,
      error: undefined,
    };
  }

  componentDidMount() {
    this.fetchData();
  }

  fetchData = async () => {
    this.setState({ loading: true });
    const { apiEndpoint, pid } = this.props;

    try {
      const response = await InvenioAdministrationActionsApi.getResource(
        apiEndpoint,
        pid
      );

      this.setState({
        loading: false,
        data: response.data,
        error: undefined,
      });
    } catch (e) {
      console.error(e);
      this.setState({ error: e });
    }
  };

  /**
   * Sorts given columns given their provided order.
   * Returns an array of objects, each object being composed as:
   * {
   *   key: str,
   *   text: str,
   *   order: number
   * }
   *
   * @param {Object[]} columns
   * @returns {Object[]} an array of objects, ordered by the provided order.
   */
  sortColumns = (columns) => {
    let sorted = [];
    Object.keys(columns).forEach((key) => {
      let innerObj = columns[key];
      if (
        Object.prototype.hasOwnProperty.call(innerObj, "text") &&
        Object.prototype.hasOwnProperty.call(innerObj, "order")
      ) {
        sorted.push({
          key: key,
          text: columns[key].text,
          order: innerObj.order,
        });
      }
    });
    return sorted.sort((a, b) => a.order > b.order);
  };

  childrenWithData = (data, columns) => {
    const { children } = this.props;
    return React.Children.map(children, (child) => {
      if (React.isValidElement(child)) {
        return React.cloneElement(child, { data: data, columns: columns });
      }
      return child;
    });
  };

  handleDelete = () => {
    // after deleting the resource go back to the list view
    const { listUIEndpoint } = this.props;
    window.location.href = listUIEndpoint;
  };

  render() {
    const {
      title,
      columns,
      actions,
      displayEdit,
      displayDelete,
      apiEndpoint,
      idKeyPath,
      listUIEndpoint,
      resourceName,
    } = this.props;
    const { loading, data, error } = this.state;

    const sortedColumns = this.sortColumns(columns);
    return (
      <ErrorPage
        error={!_isEmpty(error)}
        errorCode={error?.response.status}
        errorMessage={error?.response.data}
      >
        <Grid stackable>
          <Grid.Row columns="2">
            <Grid.Column verticalAlign="middle">
              <Header as="h1">{title}</Header>
            </Grid.Column>
            <Grid.Column
              verticalAlign="middle"
              floated="right"
              textAlign="right"
            >
              <Actions
                title={title}
                resourceName={resourceName}
                apiEndpoint={apiEndpoint}
                displayEdit={displayEdit}
                displayDelete={displayDelete}
                actions={actions}
                resource={data}
                idKeyPath={idKeyPath}
                successCallback={this.handleDelete}
                listUIEndpoint={listUIEndpoint}
              />
            </Grid.Column>
          </Grid.Row>
          <Grid.Column width="16">
            {loading ? (
              <Segment className="rel-pt-4 rel-pb-4">
                <Dimmer active inverted>
                  <Loader />
                </Dimmer>
              </Segment>
            ) : (
              <>
                <DetailsTable data={data} columns={sortedColumns} />
                {this.childrenWithData(data, columns)}
              </>
            )}
          </Grid.Column>
        </Grid>
      </ErrorPage>
    );
  }
}

AdminDetailsView.propTypes = {
  actions: PropTypes.object,
  apiEndpoint: PropTypes.string.isRequired,
  columns: PropTypes.array.isRequired,
  displayDelete: PropTypes.bool.isRequired,
  displayEdit: PropTypes.bool.isRequired,
  pid: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  children: PropTypes.object,
  resourceName: PropTypes.string.isRequired,
  idKeyPath: PropTypes.string.isRequired,
  listUIEndpoint: PropTypes.string.isRequired,
};

AdminDetailsView.defaultProps = {
  actions: undefined,
  children: undefined,
};
