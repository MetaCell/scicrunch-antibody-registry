import React, { useContext, useRef, useCallback, useEffect } from "react";
import InputBase from "@mui/material/InputBase";
import { SearchIcon, SlashIcon } from "../icons";
import { Box, Autocomplete, InputAdornment, Stack, Tooltip, Typography, Paper } from "@mui/material";
import SearchContext from "../../context/search/SearchContext";
import { useHistory } from 'react-router-dom';
import { MYSUBMISSIONS, SEARCH_MODES } from "../../constants/constants";
import { isFilterAndSortModelEmpty } from "../../utils/antibody";


const styles = {
  input: (theme) => ({
    display: "flex",
    borderRadius: theme.shape,
    backgroundColor: theme.palette.grey["100"],
    padding: theme.spacing(0.5),
    "&.Mui-focused": {
      color: 'grey.700',
      backgroundColor: 'common.white',
      border: 'solid 1px',
      borderColor: 'primary.main',
      boxShadow: '0px 0px 0px 3px #E5E9FC',
    },
    "& .MuiInputBase-root.Mui-focused": {
      "& .MuiSvgIcon-fontSizeInherit": {
        "& path": {
          stroke: '#344054'
        }
      }
    }
  }),
  slashIcon: {
    bgcolor: "grey.200",
    maxHeight: "2rem",
    minWidth: "2rem",
    borderRadius: "0.375rem",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    p: 1,
  }
}

export default function Searchbar(props) {

  const {
    getAntibodyList,
    loader,
    activeSearch,
    filterModel,
    setFilterModel,
    sortModel,
    setSortModel,
    setActiveSearch
  } = useContext(SearchContext)

  const history = useHistory();

  const ref = useRef(null);

  const autocompleteOps = [];
  const handleChange = useCallback((e: any) => {
    if (e.target.value === activeSearch) { return; }
    if (!e.target.value) {
      if (props.activeTab === MYSUBMISSIONS) {
        history.push('')
      } else {
        if (isFilterAndSortModelEmpty(filterModel, sortModel)) {
          getAntibodyList(SEARCH_MODES.ALL_ANTIBODIES);
        } else {
          getAntibodyList(SEARCH_MODES.ALL_FILTERED_AND_SEARCHED_ANTIBODIES, '', 1, filterModel, sortModel);
        }
      }
    } else {
      if (props.activeTab === MYSUBMISSIONS) {
        setActiveSearch(e.target.value)
        setFilterModel({ items: [] })
        setSortModel([])
        history.push('')
      } else {
        if (isFilterAndSortModelEmpty(filterModel, sortModel)) {
          getAntibodyList(SEARCH_MODES.SEARCHED_ANTIBODIES, e.target.value);
        } else {
          getAntibodyList(SEARCH_MODES.ALL_FILTERED_AND_SEARCHED_ANTIBODIES, e.target.value, 1, filterModel, sortModel);
        }
      }
    }
  }, [getAntibodyList, history, activeSearch, filterModel, sortModel, props.activeTab, setActiveSearch, setFilterModel, setSortModel]);

  const handleKeyPress = useCallback((event) => {
    if (event.key === '/') {
      event.preventDefault()
      ref.current?.focus()

    }
  }, []);

  useEffect(() => {
    document.addEventListener('keydown', handleKeyPress);

    return () => {
      document.removeEventListener('keydown', handleKeyPress);
    };
  }, [handleKeyPress]);


  return (<Stack direction="row" className="search-bar">
    <Tooltip sx={{ opacity: 0.5 }} title={<Paper elevation={1} sx={{ p: 1 }}><Typography sx={{ fontSize: "0.8rem", mb: 1 }}>
      <strong>Search tips:</strong>
      <Typography component="ul" sx={{ fontSize: "0.8rem", textAlign: "left" }}>
        <li>Catalog number is searched first if you type numbers</li>
        <li>Anything else is searched if no catalog number matches</li>
        <li>If you are having trouble, please check <a href="//rrid.site">rrid.site</a></li>

      </Typography>
    </Typography></Paper>}>
      <Autocomplete
        sx={styles.input}
        freeSolo
        options={autocompleteOps.map(option => option)}
        fullWidth
        clearOnEscape
        disabled={loader}
        className="search-autocomplete"
        value={activeSearch}
        renderInput={(params) => {
          const { InputProps, ...rest } = params;

          return (
            <InputBase
              id="search-main"
              inputRef={ref}

              {...InputProps}

              {...rest}
              placeholder="Search antibodies"

              startAdornment={<SearchIcon fontSize="inherit" sx={{ mx: "0.65rem" }} />}
              endAdornment={
                InputProps.endAdornment ? InputProps.endAdornment :
                  <InputAdornment position='end'>
                    <Box
                      sx={styles.slashIcon}
                    >
                      <SlashIcon sx={{ width: '1rem', height: '1rem' }} />
                    </Box>
                  </InputAdornment>
              }
              inputProps={{
                ...rest.inputProps,
                onBlur: handleChange,
                onKeyDown: (e) => e.key === "Enter" && handleChange(e)

              }}
            />
          )
        }
        }
      />
    </Tooltip>
  </Stack>
  );
}