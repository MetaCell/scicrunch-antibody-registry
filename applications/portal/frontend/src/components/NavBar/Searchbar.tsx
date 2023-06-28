import React, { useContext, useRef, useCallback, useEffect } from "react";
import {  useTheme } from "@mui/material/styles";
import InputBase from "@mui/material/InputBase";
import { SearchIcon, SlashIcon } from "../icons";
import { Box, Autocomplete, InputAdornment, Stack, Tooltip, Typography, Paper } from "@mui/material";
import SearchContext from "../../context/search/SearchContext";
import { useHistory } from 'react-router-dom'; 


const styles={
  input: (theme) => ({
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
  }),
  slashIcon:{
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

export default function Searchbar() {

  const { getFilteredAntibodies, clearSearch, loader, activeSearch } = useContext(SearchContext)

  const history = useHistory();

  const ref= useRef(null);

  const autocompleteOps=[]

  const handleChange=useCallback((e: any) => {
    if(e.target.value === activeSearch) {return;}
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

  
  return (<Stack direction="row" className="search-bar">
    <Tooltip sx={{ opacity: 0.5 }}   title={<Paper elevation={1} sx={{ p:1 }}><Typography sx={{ fontSize: "0.8rem", mb: 1 }}>
      <strong>Search tips:</strong>
      <Typography component="ul" sx={{ fontSize: "0.8rem", textAlign: "left" }}>
        <li>Catalog number is searched first if you type numbers</li>
        <li>Anything else is searched if no catalog number matches</li>
        <li>Search results are currently limited to a maximum of 100 elements; refine your search if you don&apos;t find what you&apos;re looking for (table filters <b>do not</b> refine the search)</li>
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
       
        renderInput={(params) => { 
          const  { InputProps, ...rest } = params;
  
          return(
            <InputBase 
              id="search-main"
              inputRef={ref}
              {...InputProps}
                
              {...rest}  
              placeholder="Search antibodies" 
                
              startAdornment={<SearchIcon fontSize="inherit"sx={{ mx: "0.65rem" }}/>}
              endAdornment={
                InputProps.endAdornment? InputProps.endAdornment:
                  <InputAdornment position='end'>
                    <Box
                      sx={styles.slashIcon}
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
