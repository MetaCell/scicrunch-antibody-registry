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


  const { getFilteredAntibodies, clearSearch, activeSearch } = useContext(SearchContext)

  const history = useHistory();
  const isInitialRender = useRef(true);
  const ref= useRef(null);

  const autocompleteOps=[]

  const handleChange=(e:React.SyntheticEvent, value:string| null) => {
    !value? clearSearch():getFilteredAntibodies(value)
  }

  const handleInputChange =(e) => {
    if (e.target.matches('li')) {return null}
    !e.target.value? clearSearch():
      getFilteredAntibodies(e.target.value)
  }

  const debouncedChangeHandler = useMemo(
    () => debounce(handleInputChange, 1000)
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

        <Autocomplete  
          sx={classes.input} 
          freeSolo 
          options={autocompleteOps.map(option => option)} 
          onChange={handleChange}
          onInputChange={debouncedChangeHandler}
          fullWidth
          clearOnEscape
          renderInput={(params) => { 
            const  { InputProps,InputLabelProps, ...rest } = params
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
