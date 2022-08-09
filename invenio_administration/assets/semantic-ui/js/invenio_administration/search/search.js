/*
 * This file is part of Invenio.
 * Copyright (C) 2022 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import { createSearchAppInit } from "@js/invenio_search_ui";
import { SearchFacets } from "./SearchFacets";
import { SearchResultItem } from "./SearchResultItem";
import { SearchBarElement } from "./SearchBarElement";
import SearchEmptyResults from "./SearchEmptyResults";
import { SearchResultsContainer } from "./SearchResultsContainer";
import { SearchResults } from "./SearchResults";
import { parametrize } from "react-overridable";
import { DropdownSort } from "@js/invenio_search_ui/components";

const domContainer = document.getElementById("invenio-search-config");
const columns = JSON.parse(domContainer.dataset.columns);

const ResultsContainerWithConfig = parametrize(SearchResultsContainer, {
  columns: columns,
});

const SearchResultsWithConfig = parametrize(SearchResults, {
  columns: columns,
});

const SearchResultItemWithConfig = parametrize(SearchResultItem, {
  columns: columns,
});

const overwriteComponents = {
  "ResultsList.item": SearchResultItemWithConfig,
  "ResultsGrid.item": () => {},
  // "SearchApp.layout": PublicMembersSearchLayout,
  "SearchBar.element": SearchBarElement,
  "SearchApp.results": SearchResultsWithConfig,
  "ResultsList.container": ResultsContainerWithConfig,
  "EmptyResults.element": SearchEmptyResults,
  "Sort.element": DropdownSort,
  "SearchApp.facets": SearchFacets,
};

createSearchAppInit(overwriteComponents);
