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
import SearchEmptyResults from "./SearchEmptyResults";
import { SearchResultsContainer } from "./SearchResultsContainer";
import { SearchResults } from "./SearchResults";
import { parametrize } from "react-overridable";
import { DropdownSort } from "@js/invenio_search_ui/components";
import { SearchResultOptions } from "./SearchResultOptions";
import { SearchBar } from "./SearchBarElement";

const domContainer = document.getElementById("invenio-search-config");

const sortColumns = (columns) =>
  Object.entries(columns).sort((a, b) => a[1].order > b[1].order);
const columns = JSON.parse(domContainer.dataset.fields);
const sortedColumns = sortColumns(columns);
const displaySearch = JSON.parse(domContainer.dataset.displaySearch);

const ResultsContainerWithConfig = parametrize(SearchResultsContainer, {
  columns: sortedColumns,
});

const SearchResultsWithConfig = parametrize(SearchResults, {
  columns: sortedColumns,
});

const SearchResultItemWithConfig = parametrize(SearchResultItem, {
  columns: sortedColumns,
});

const overwriteComponents = {
  "ResultsList.item": SearchResultItemWithConfig,
  "ResultsGrid.item": () => {},
  "SearchApp.results": SearchResultsWithConfig,
  "ResultsList.container": ResultsContainerWithConfig,
  "EmptyResults.element": SearchEmptyResults,
  "Sort.element": DropdownSort,
  "SearchApp.facets": SearchFacets,
  "SearchApp.searchbarContainer": () => null,
  "SearchApp.resultOptions": SearchResultOptions,
  SearchBar: displaySearch ? SearchBar : () => null,
};

createSearchAppInit(overwriteComponents);
