import * as React from "react";
import MobileStepper from "@mui/material/MobileStepper";
import Button from "@mui/material/Button";
import { Typography } from "@mui/material";
import { useTheme } from "@mui/system";

export default function Stepper({ activeStep, totalSteps }) {
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
  const stepsTitle = [
    "Type of Antibody",
    "Product Page Link",
    "Antibody Details",
  ];
  return (
    <MobileStepper
      variant="progress"
      steps={totalSteps}
      position="static"
      activeStep={activeStep}
      sx={classes.paper}
      nextButton={
        <Typography variant="subtitle1" sx={classes.paper}>
          Step {activeStep}:{" "}
          {activeStep === 1
            ? stepsTitle[0]
            : totalSteps === 3
            ? stepsTitle[2]
            : stepsTitle[activeStep - 1]}
        </Typography>
      }
      backButton={<Button sx={{ display: "none" }}></Button>}
    />
  );
}
