import React from "react";
import ReactDOM from "react-dom";
import { EditPage } from "./EditPage";
import _get from "lodash/get";

const domContainer = document.getElementById(
  "invenio-administration-edit-root"
);
const resourceSchema = JSON.parse(domContainer.dataset.resourceSchema);
const apiEndpoint = _get(domContainer.dataset, "apiEndpoint");
const pid = JSON.parse(domContainer.dataset.pid);

ReactDOM.render(
  <EditPage
    resourceSchema={resourceSchema}
    apiEndpoint={apiEndpoint}
    pid={pid}
  />,
  domContainer
);
