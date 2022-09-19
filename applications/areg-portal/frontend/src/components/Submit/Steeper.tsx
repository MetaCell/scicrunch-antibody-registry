import * as React from "react";
import MobileStepper from "@mui/material/MobileStepper";
import Button from "@mui/material/Button";
import { Typography } from "@mui/material";

export default function Stepper({ activeStep, totalSteps }) {
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
      sx={{ maxWidth: 400, flexGrow: 1 }}
      nextButton={
        <Typography
          variant="subtitle1"
          sx={{ color: "grey.700", fontWeight: 500 }}
        >
          Step {activeStep + 1}:{" "}
          {activeStep === 0
            ? stepsTitle[0]
            : totalSteps === 2
            ? stepsTitle[2]
            : stepsTitle[activeStep]}
        </Typography>
      }
      backButton={<Button sx={{ display: "none" }}></Button>}
    />
  );
}
