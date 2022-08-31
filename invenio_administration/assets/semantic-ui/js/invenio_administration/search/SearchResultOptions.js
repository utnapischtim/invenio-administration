import React from "react";
import { Grid } from "semantic-ui-react";
import { i18next } from "@translations/invenio_search_ui/i18next";
import { Sort, SearchBar } from "react-searchkit";
import PropTypes from "prop-types";

export const SearchResultOptions = ({ sortOptions, sortOrderDisabled }) => {
  return (
    <Grid stackable padded relaxed>
      <Grid.Row verticalAlign="bottom">
        <Grid.Column
          className="pl-0"
          textAlign="left"
          largeScreen={12}
          computer={12}
          tablet={10}
          mobile={16}
        >
          <SearchBar />
        </Grid.Column>
        <Grid.Column
          className="pr-0"
          textAlign="right"
          largeScreen={4}
          computer={4}
          tablet={6}
          mobile={16}
        >
          {sortOptions && (
            <Sort
              sortOrderDisabled={sortOrderDisabled}
              values={sortOptions}
              ariaLabel={i18next.t("Sort")}
              label={(cmp) => (
                <>
                  {cmp}
                </>
              )}
            />
          )}
        </Grid.Column>
      </Grid.Row>
    </Grid>
  );
};

SearchResultOptions.propTypes = {
  sortOptions: PropTypes.array.isRequired,
  sortOrderDisabled: PropTypes.bool,
};

SearchResultOptions.defaultProps = {
  sortOrderDisabled: false
}
