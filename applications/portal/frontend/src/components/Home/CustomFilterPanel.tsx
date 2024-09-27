import React, { useContext, useState } from "react";
import { Box, Button, FormControl, Chip, MenuItem, TextField, IconButton, Stack } from "@mui/material";
import {
  GridCloseIcon,
} from "@mui/x-data-grid";
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { getFilterOperators, getRandomId, shouldEmptyFilterValue } from "../../utils/antibody";
import { BLANK_FILTER_MODEL } from "../../constants/constants";
import { SearchCriteriaOptions } from "../../rest";
import searchContext from "../../context/search/SearchContext";



export const CustomFilterPanel = (
  {
    columns,
    filterModel,
    setFilterModel,
    applyFilters,
  }) => {

  const { activeSearch } = useContext(searchContext);

  const filterableColumns = columns.filter((column) => {
    return column.filterable !== false && column.type !== "actions";
  });

  const handleFilterSet = (filterSet) => {
    let isFilterSetPresent = false;
    filterModel.items.forEach((item, index) => {
      if (item.id === filterSet.id) {
        filterModel.items[index] = filterSet;
        isFilterSetPresent = true;
      }
    });
    if (!isFilterSetPresent) {
      filterModel.items.push(filterSet);
    }
    setFilterModel({ ...filterModel });

    // handleSetFilterAPI({ ...filterModel, items: filterModel.items });
  }

  const removeFilterSet = (filterSet) => {
    const newFilterModelItems = filterModel.items.filter((item) => {
      return item.id !== filterSet.id;
    });
    setFilterModel({ ...filterModel, items: newFilterModelItems });
    // handleSetFilterAPI({ ...filterModel, items: newFilterModelItems });
  }

  const setEmptyFilterSet = () => {
    let newFilterModelItems = filterModel.items;
    let newBlankFilter = { ...BLANK_FILTER_MODEL, id: getRandomId() };

    newFilterModelItems = filterModel.items.concat(newBlankFilter);
    setFilterModel({ ...filterModel, items: newFilterModelItems });
  }

  return (
    (<Box sx={{
      width: "100%"
    }}>
      {
        filterModel && filterModel.items.map((filterSet, index) => (
          <Box key={index}>
            <CustomFilterRow
              columns={filterableColumns}
              filterSet={filterSet}
              handleFilterSet={handleFilterSet}
              removeFilterSet={removeFilterSet}
            />
          </Box>
        ))
      }
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          width: "100%"
        }}>
        <Button
          variant="text"
          onClick={() => {
            setEmptyFilterSet();
          }}
          sx={{ m: 1 }}
        >
          Add Filter
        </Button>

        <Button
          variant="outlined"
          color="primary"
          onClick={() => {
            applyFilters(filterModel, activeSearch);
          }}
          sx={{ m: 1 }}
        >
          Apply
        </Button>
      </Box>
    </Box>)
  );
}

const CustomFilterRow = ({ columns, filterSet, handleFilterSet, removeFilterSet } ) => {

  const [inputvalue, setInputValue] = useState(filterSet.value);


  const changeOperator = (operation) => {
    if (shouldEmptyFilterValue(filterSet, operation)) {
      handleFilterSet({ ...filterSet, operatorValue: operation, value: "" });
    } else {
      handleFilterSet({ ...filterSet, operatorValue: operation });
    }
  }
  const operatorsWithSingleInput = [
    SearchCriteriaOptions.Contains,
    SearchCriteriaOptions.Equals,
    SearchCriteriaOptions.EndsWith,
    SearchCriteriaOptions.StartsWith,
  ];
  const operators = getFilterOperators();
  return (
    (<Stack
          direction="row"
          spacing={1}
          sx={{
            display: "flex",
            alignItems: "center",
            m: 1
          }}>
      {/* 3 parts of a filter */}
      {/* columns */}
      <IconButton onClick={() => removeFilterSet(filterSet)}>
        <GridCloseIcon fontSize="small"/>
      </IconButton>
      <Select
        value={filterSet.columnField}
        onChange={(e: SelectChangeEvent) => handleFilterSet({ ...filterSet, columnField: e.target.value })}
        size="small"
        sx={{ 
          width: "12em",
          '& .MuiSelect-select': {
            textAlign: 'left'
          }
        }}
      >
        {columns.map((column) => (
          <MenuItem key={column.field} value={column.field}>
            {column.headerName}
          </MenuItem>
        ))}
      </Select>
      {/* operators */}
      <Select
        value={filterSet.operatorValue}
        onChange={(e: SelectChangeEvent) => changeOperator(e.target.value)}
        size="small"
        sx={{ 
          width: "8em",
          '& .MuiSelect-select': {
            textAlign: 'left'
          }
        }}
      >
        {Object.keys(operators).map((op) => (
          <MenuItem key={op} value={op}>
            {operators[op]}
          </MenuItem>
        ))}
      </Select>
      {/* multi-input: conditional */}
      {
        filterSet.operatorValue === SearchCriteriaOptions.IsAnyOf && (
          <CustomMultiInputWithChip
            filterSet={filterSet}
            handleFilterSet={handleFilterSet}
          />
        )
      }
      {/* input: conditional */}
      {
        operatorsWithSingleInput.includes(filterSet.operatorValue) && (
          <TextField
            value={inputvalue}
            size="small"
            variant="outlined"
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleFilterSet({ ...filterSet, value: inputvalue });
              }
            }}
            onMouseLeave={() => handleFilterSet({ ...filterSet, value: inputvalue })}
            sx={{ width: "12em" }}
          />
        )

      }
    </Stack>)
  );
}

const CustomMultiInputWithChip = ({ filterSet, handleFilterSet }) => {

  const [values, setValues] = useState(filterSet.value || []);
  const [currValue, setCurrValue] = useState("");

  const handleKeyUp = (e) => {
    if (e.key === "Enter" && e.target.value) {
      let arr = [...values]
      arr.push(e.target.value)
      handleFilterSet({ ...filterSet, value: arr });
      setValues(arr);
      setCurrValue("");
    }
  };
  const handleDelete = (item, index) => {
    let arr = [...values]
    arr.splice(index, 1)
    setValues(arr)
    handleFilterSet({ ...filterSet, value: arr });
  }
  const handleChange = (e) => {
    setCurrValue(e.target.value);
  };
  return (
    <FormControl>
      <Box className={"container"}>
        {filterSet.value && filterSet.value?.map((item, index) => (
          <Chip key={index} size="small" onDelete={() => handleDelete(item, index)} label={item} />
        ))}
      </Box>
      <TextField
        value={currValue}
        variant="outlined"
        onChange={handleChange}
        onKeyDown={handleKeyUp}
        onBlur={handleKeyUp}
      />
    </FormControl>

  )
}
