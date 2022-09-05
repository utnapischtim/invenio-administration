import React from "react";
import ReactDOM from "react-dom";
import { CreatePage } from "./CreatePage";
import _get from "lodash/get";

const domContainer = document.getElementById(
  "invenio-administration-create-root"
);
const resourceSchema = JSON.parse(domContainer.dataset.resourceSchema);
const apiEndpoint = _get(domContainer.dataset, "apiEndpoint");

ReactDOM.render(
  <CreatePage resourceSchema={resourceSchema} apiEndpoint={apiEndpoint} />,
  domContainer
);
