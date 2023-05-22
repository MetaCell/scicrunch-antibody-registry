import React, { useContext, useRef, useCallback, useEffect } from "react";
import {  useTheme } from "@mui/material/styles";
import InputBase from "@mui/material/InputBase";
import { SearchIcon, SlashIcon } from "../icons";
import { Box, Autocomplete, InputAdornment, Stack, Tooltip, Typography } from "@mui/material";
import SearchContext from "../../context/search/SearchContext";
import { useHistory } from 'react-router-dom';


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

  const handleChange=useCallback((e: any) => {
    if(!e.target.value){
      clearSearch()
    } else {
      history.push('/');
      getFilteredAntibodies(e.target.value)
    }
  }, [getFilteredAntibodies, clearSearch, history]);

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

  
  return (<Stack direction="row">
    <Tooltip sx={{ opacity: 0.5 }}   title={<Typography sx={{ fontSize: "0.8rem", mb: 1 }}>
      Search tips:
      <Typography component="ul" sx={{ fontSize: "0.8rem", textAlign: "left" }}>
        <li>Catalog number is searched first if you type numbers</li>
        <li>Anything else is searched if no catalog number matches</li>
        <li>Search is currently limited to a maximum of 100 elements; refine your search if you don't find what you're looking for with the filters</li>
        
      </Typography>
    </Typography>}>
      <Autocomplete  
        sx={classes.input} 
        freeSolo 
        options={autocompleteOps.map(option => option)} 
        fullWidth
        clearOnEscape
        disabled={loader}
       
        renderInput={(params) => { 
          const  { InputProps, ...rest } = params;
  
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
              inputProps =  {{
                ...rest.inputProps,
                onBlur: handleChange,
                onKeyDown: (e) =>  e.key === "Enter" && handleChange(e)
                
              } }
            />
          )
        }
        }
      />

    </Tooltip>

  </Stack>
  );
}
