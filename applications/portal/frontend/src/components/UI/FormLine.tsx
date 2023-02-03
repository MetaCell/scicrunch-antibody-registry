import React from "react";
import Grid from "@mui/material/Grid";

const FormLine = ({ children }) => {
  const child = React.Children.toArray(children) as React.ReactElement[];
  return (
    <Grid container spacing={3}>
      <Grid item lg={6}>
        {child[0]}
      </Grid>
      <Grid item lg={6}>
        {child[1]}
      </Grid>
    </Grid>
  );
};

export default FormLine;
