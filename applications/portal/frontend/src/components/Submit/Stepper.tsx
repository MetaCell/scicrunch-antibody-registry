import * as React from "react";
import MobileStepper from "@mui/material/MobileStepper";
import Button from "@mui/material/Button";
import { Typography } from "@mui/material";

export default function Stepper({ activeStep }) {

  const styles = {
    paper: {
      maxWidth: 400,
      flexGrow: 1,
      "& .MuiLinearProgress-colorPrimary": {
        backgroundColor: (theme) => theme.palette.grey[200],
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
      sx={styles.paper}
      className="stepper"
      nextButton={
        <Typography variant="subtitle1" sx={styles.paper} className={`step-${activeStep}`}>
          Step {activeStep}/2:
          {stepsTitle[activeStep - 1]}
        </Typography>
      }
      backButton={<Button sx={{ display: "none" }}></Button>}
    />
  );
}
