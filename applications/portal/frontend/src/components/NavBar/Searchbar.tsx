import React, { useContext, useEffect, useRef, useCallback, useMemo } from "react";
import { styled } from "@mui/material/styles";
import InputBase from "@mui/material/InputBase";
import { SearchIcon, SlashIcon } from "../icons";
import { Box, Stack, Autocomplete } from "@mui/material";
import SearchContext from "../../context/search/SearchContext";
import { useHistory } from 'react-router-dom';
import debounce from 'lodash.debounce';

const Search = styled("div")(({ theme }) => ({
  display: "flex",
  flexGrow: 1,
  borderRadius: theme.shape.borderRadius,
  backgroundColor: theme.palette.grey["100"],
  padding: theme.spacing(0.5),
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: theme.palette.grey["600"],
  width: "100%",
  fontSize: "1rem",
  "& .MuiInputBase-input": {
    transition: theme.transitions.create("width"),
    width: "100%",
  },
}));



export default function Searchbar() {

  const { getFilteredAntibodies, clearSearch, activeSearch } = useContext(SearchContext)

  const history = useHistory();
  const isInitialRender = useRef(true);
  const ref= useRef(null);

  const autocompleteOps=['0']

  const handleChange=(e:React.SyntheticEvent, value:string| null) => {
    value? getFilteredAntibodies(e.target):null
  }

  const handleInputChange =(e) => {
    !e.target.value? clearSearch():
      getFilteredAntibodies(e.target.value)
  }

  const debouncedChangeHandler = useMemo(
    () => debounce(handleInputChange, 500)
    , []);

  useEffect(() => {
    !isInitialRender.current?
      history.push('/'):
      isInitialRender.current = false
      
  }, [activeSearch])

  const handleKeyPress = useCallback((event) => {
    if(event.key==='/'){
      event.preventDefault()
      ref.current.focus()
   
    }
  }, []);

  useEffect(() => {
    document.addEventListener('keydown', handleKeyPress);

    return () => {
      document.removeEventListener('keydown', handleKeyPress);
    };
  }, [handleKeyPress]);
  
  return (<>
    <Search>
      <Stack
        direction="row"
        spacing={1}
        display="flex"
        alignItems="center"
        width="100%"
        sx={{ ml: 1 }}
      >
        <SearchIcon
          sx={{ width: "1.125rem", height: "1.125rem", m: "0.125rem" }}
        />
        <Autocomplete  sx={{ width:'100%' }} freeSolo options={autocompleteOps.map(option => option)} 
          onChange={handleChange} onInputChange={debouncedChangeHandler}renderInput={(params) => { const  { InputProps,...rest } = params
            return(<StyledInputBase inputRef={ref}
              {...InputProps} {...rest}  placeholder="Search for catalog number"
            />)}}/>
        <Box
          sx={(theme) => ({
            bgcolor: "grey.200",
            maxHeight: "2rem",
            minWidth: "2rem",
            borderRadius: "0.375rem",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            p: theme.spacing(1),
          })}
        >
          <SlashIcon sx={{ width: "1rem", height: "1rem" }} />
        </Box>
      </Stack>
    </Search>
  </>
  );
}
