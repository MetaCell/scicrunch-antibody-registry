import React, { useState } from "react";
import {
  Button,
  Dialog,
  DialogContent,
  DialogTitle,
  Grid,
  Box,
  Typography,
  TextField,
  MenuItem,
  Divider,
} from "@mui/material";

const filterByFields = ["Target antigen", "ID", "Vendor"];
const filterOperatorOptions = ["contains", "equals"];

const FilterModal = (props) => {
  const { onClose, open } = props;

  const [filterBy, setFilterBy] = useState("Target antigen");
  const [filterOperator, setFilterOperator] = useState("equals");

  return (
    <Dialog onClose={onClose} open={open}>
      <Box sx={{ py: 1, px: 1 }}>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Typography px="4px" variant="subtitle2">
            Filter
          </Typography>
          <Button>
            <Typography variant="subtitle2">Clear Filter</Typography>
          </Button>
        </Box>
      </Box>
      <Divider />
      <Box sx={{ py: 1, px: 1 }}>
        <Grid container spacing={1}>
          <Grid item xs={4}>
            <TextField select value={filterBy}>
              {filterByFields.map((ele, index) => (
                <MenuItem key={index} value={ele}>
                  {ele}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={4}>
            <TextField
              select
              value={filterOperator}
              sx={{ width: "100%", textAlign: "left" }}
            >
              {filterOperatorOptions.map((ele, index) => (
                <MenuItem key={index} value={ele}>
                  {ele}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={4}>
            <TextField placeholder="Value"></TextField>
          </Grid>
        </Grid>
      </Box>
    </Dialog>
  );
};

export default FilterModal;
