import React, { useContext, useEffect, useRef, useCallback, useMemo } from "react";
import {  useTheme } from "@mui/material/styles";
import InputBase from "@mui/material/InputBase";
import { SearchIcon, SlashIcon } from "../icons";
import { Box, Autocomplete, InputAdornment } from "@mui/material";
import SearchContext from "../../context/search/SearchContext";
import { useHistory } from 'react-router-dom';
import debounce from 'lodash.debounce';


export default function Searchbar() {

  const theme = useTheme()
  const classes={
    input:{
      display: "flex",
      borderRadius: theme.shape,
      backgroundColor: theme.palette.grey["100"],
      padding: theme.spacing(0.5),
      "&.Mui-focused":{
        color:'grey.700',
        backgroundColor:'common.white',
        border:'solid 1px',
        borderColor:'primary.main',
        boxShadow: '0px 0px 0px 3px #E5E9FC',
      },
      "& .MuiInputBase-root.Mui-focused":{ 
        "& .MuiSvgIcon-fontSizeInherit":{
          "& path":{
            stroke:'#344054'
          }   
        }
      }
    },
    slashIcon:{
      bgcolor: "grey.200",
      maxHeight: "2rem",
      minWidth: "2rem",
      borderRadius: "0.375rem",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      p: theme.spacing(1),
    }
  }


  const { getFilteredAntibodies, clearSearch, loader } = useContext(SearchContext)

  const history = useHistory();

  const ref= useRef(null);

  const autocompleteOps=[]

  const handleChange=useCallback((e:React.SyntheticEvent, value:string| null) => {
    if(!value){
      clearSearch()
    } else {
      history.push('/');
      getFilteredAntibodies(value)
    }
  }, [getFilteredAntibodies, clearSearch, history]);


  const debouncedChangeHandler = useMemo(
    () => debounce((e: any) => {
      if (e.target.matches('li')) {return null}
      return handleChange(null, e.target.value)}, 1000)
    , [handleChange]);


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

        <Autocomplete  
          sx={classes.input} 
          freeSolo 
          options={autocompleteOps.map(option => option)} 
          onChange={handleChange}
          onInputChange={debouncedChangeHandler}
          fullWidth
          clearOnEscape
          disabled={loader}
          renderInput={(params) => { 
            const  { InputProps, ...rest } = params
            return(
              <InputBase 
                inputRef={ref}
                {...InputProps}
                {...rest}  
                placeholder="Search for catalog number" 
                startAdornment={<SearchIcon fontSize="inherit"sx={{ mx: "0.65rem" }}/>}
                endAdornment={
                  InputProps.endAdornment? InputProps.endAdornment:
                    <InputAdornment position='end'>
                      <Box
                        sx={classes.slashIcon}
                      >
                        <SlashIcon  sx={{ width:'1rem', height:'1rem' }}/>
                      </Box>
                    </InputAdornment>
                }
              />
            )
          }
          }
        />

  </>
  );
}
