import { Grid } from "@mui/material";
import React from "react";
import AntibodyDetailsForm from "./AntibodyDetailsForm";
const Index = () => {
    return (
        <Grid container sx={{ marginTop: "100px" }} justifyContent="center" alignItems="center">
            <AntibodyDetailsForm />
        </Grid>
    )
}
export default Index;