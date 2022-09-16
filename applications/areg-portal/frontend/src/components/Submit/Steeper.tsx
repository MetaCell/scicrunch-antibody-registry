import * as React from "react";
import MobileStepper from "@mui/material/MobileStepper";
import Button from "@mui/material/Button";
import { Typography } from "@mui/material";

export default function Stepper({ activeStep }) {
  const stepsTitle = [
    "Type of Antibody",
    "Product Page Link",
    "Antibody Details",
  ];
  return (
    <MobileStepper
      variant="progress"
      steps={3}
      position="static"
      activeStep={activeStep}
      sx={{ maxWidth: 400, flexGrow: 1 }}
      nextButton={
        <Typography
          variant="subtitle1"
          sx={{ color: "grey.700", fontWeight: 500 }}
        >
          Step {activeStep + 1}/3: {stepsTitle[activeStep]}
        </Typography>
      }
      backButton={<Button sx={{ display: "none" }}></Button>}
    />
  );
}
