// TODO remove this rule disable when this module is implemented. Otherwise eslint tests will fail.
/* eslint-disable no-unused-vars */
import { APIRoutes } from "./routes";
import { http } from "./config";

const getResource = async (apiEndpoint, pid) => {
  return await http.get(APIRoutes.get(apiEndpoint, pid));
};

const deleteResource = async (resource, apiEndpoint, idKeyPath = "pid") => {
  return await http.delete(
    APIRoutes.detailsView(apiEndpoint, resource, idKeyPath)
  );
};

const editResource = async (apiEndpoint, pid, payload) =>
  await http.put(APIRoutes.get(apiEndpoint, pid), payload);

const createResource = () => {};

const performCustomAction = () => {};

export const InvenioAdministrationActionsApi = {
  deleteResource: deleteResource,
  editResource: editResource,
  getResource: getResource,
};
