import React, { useState } from "react";
import { Box, Button, FormControl, Input, Chip } from "@mui/material";
import {
  GridCloseIcon,
} from "@mui/x-data-grid";
import { getFilterRequestMap, getRandomId } from "../../utils/antibody";
import { BLANK_FILTER_MODEL } from "../../constants/constants";
import { makeStyles } from "@mui/styles";


const useStyles = makeStyles((theme) => ({
  formControlRoot: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    width: "300px",
    flexWrap: "wrap",
    flexDirection: "row",
    border: '2px solid lightgray',
    padding: 4,
    borderRadius: '4px',
    "&> div.container": {
      gap: "6px",
      display: "flex",
      flexDirection: "row",
      flexWrap: "wrap"
    },
    "& > div.container > span": {
      backgroundColor: "gray",
      padding: "1px 3px",
      borderRadius: "4px"
    }
  }
}));



export const CustomFilterPanel = (props) => {
  const {
    columns,
    filterModel,
    setFilterModel,
    handleSetFilterAPI,
  } = props;

  const filterableColumns = columns.filter((column) => column.field !== "nameAndId");

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

    handleSetFilterAPI({ ...filterModel, items: filterModel.items });
  }

  const removeFilterSet = (filterSet) => {
    const newFilterModelItems = filterModel.items.filter((item) => {
      return item.id !== filterSet.id;
    });
    handleSetFilterAPI({ ...filterModel, items: newFilterModelItems });
  }

  const setEmptyFilterSet = () => {
    let newFilterModelItems = filterModel.items;
    let newBlankFilter = { ...BLANK_FILTER_MODEL, id: getRandomId() };

    newFilterModelItems = filterModel.items.concat(newBlankFilter);
    setFilterModel({ ...filterModel, items: newFilterModelItems });
  }

  return (
    <Box>
      {
        filterModel && filterModel.items.map((filterSet, index) => (
          <div key={index}>
            <CustomFilterRowPanel
              columns={filterableColumns}
              filterSet={filterSet}
              handleFilterSet={handleFilterSet}
              removeFilterSet={removeFilterSet}
            />
          </div>
        ))
      }
      <Box>
        <Button
          variant="outlined"
          onClick={() => {
            setEmptyFilterSet();
          }}
          sx={{ m: 1, float: "left" }}
        >
          New Filter
        </Button>
      </Box>
    </Box>
  )
}

const CustomFilterRowPanel = (props) => {
  const { columns, filterSet, handleFilterSet, removeFilterSet } = props;
  const [inputvalue, setInputValue] = useState(filterSet.value);
  const classes = useStyles();


  // ----- Multi input file -----
  const [values, setValues] = useState(filterSet.value || []);
  const [currValue, setCurrValue] = useState("");

  const handleKeyUp = (e) => {
    if (e.key === "Enter") {
      values.push(e.target.value)
      handleFilterSet({ ...filterSet, value: values });
      setValues(values);
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
  // ----- Multi input file -----

  return (
    <Box>
      {/* 3 parts of a filter */}
      <GridCloseIcon
        onClick={() => removeFilterSet(filterSet)}
        sx={{ cursor: "pointer" }}
      />
      {/* columns */}
      <select
        value={filterSet.columnField}
        onChange={(e) => handleFilterSet({ ...filterSet, columnField: e.target.value })}
      >
        {columns.map((column) => (
          <option key={column.field} value={column.field}>
            {column.headerName}
          </option>
        ))}
      </select>

      {/* operators */}
      <select
        value={filterSet.operatorValue}
        onChange={(e) => handleFilterSet({ ...filterSet, operatorValue: e.target.value })}
      >
        {Object.keys(getFilterRequestMap()).map((operator) => (
          <option key={operator} value={operator}>
            {operator}
          </option>
        ))}
      </select>


      {/* multi-input: conditional */}
      {
        // if the operator is isAnyOf then we show a multi-select input field
        filterSet.operatorValue === "isAnyOf" && (
          <FormControl classes={{ root: classes.formControlRoot }}>
            <div className={"container"}>
              {filterSet.value && filterSet.value.map((item, index) => (
                <Chip key={index} size="small" onDelete={() => handleDelete(item, index)} label={item} />
              ))}
            </div>
            <Input
              value={currValue}
              onChange={handleChange}
              onKeyDown={handleKeyUp}
              onBlur={handleKeyUp}
            />
          </FormControl>

        )
      }

      {/* input: conditional */}
      {
        ["contains", "equals", "endsWith", "startsWith"].includes(filterSet.operatorValue) && (
          <Input
            value={inputvalue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleFilterSet({ ...filterSet, value: inputvalue });
              }
            }}
            onBlur={() => handleFilterSet({ ...filterSet, value: inputvalue })}
          />
        )

      }

    </Box>
  )
}

