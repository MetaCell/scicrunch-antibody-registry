import * as React from "react";
import MobileStepper from "@mui/material/MobileStepper";
import Button from "@mui/material/Button";
import { Typography } from "@mui/material";
import { useTheme } from "@mui/system";

export default function Stepper({ activeStep }) {
  const theme = useTheme();
  const classes = {
    paper: {
      maxWidth: 400,
      flexGrow: 1,
      "& .MuiLinearProgress-colorPrimary": {
        backgroundColor: theme.palette.grey[200],
        borderRadius: "0.25rem",
        height: "0.5rem",
      },
    },
  };
  const stepsTitle = ["Type of Antibody", "Antibody Details"];
  return (
    <MobileStepper
      variant="progress"
      steps={3}
      position="static"
      activeStep={activeStep}
      sx={classes.paper}
      nextButton={
        <Typography variant="subtitle1" sx={classes.paper}>
          Step {activeStep}/2:
          {stepsTitle[activeStep - 1]}
        </Typography>
      }
      backButton={<Button sx={{ display: "none" }}></Button>}
    />
  );
}
