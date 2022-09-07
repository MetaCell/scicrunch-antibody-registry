import React from "react";
import {
  Box,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Typography,
} from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { StepIcon } from "../icons";

const historySteps = [
  {
    label: "07/23/2022 (Current version)",
    description: "Latest update",
  },
  {
    label: "04/23/2022",
    description: "Antibody approved",
  },
  {
    label: "04/21/2022",
    description: "Antibody Submitted",
  },
];

const HistoryStepper = (props) => {
  let { classes, antibody } = props;
  const theme = useTheme();

  classes = {
    ...classes,
    container: {
      backgroundColor: theme.palette.grey[50],
      padding: theme.spacing(1, 2),
      marginTop: theme.spacing(3),
      borderRadius: theme.shape,
    },
    step: {
      color: theme.palette.primary.main,

      "& .MuiStepLabel-label": {
        fontSize: "0.875rem",
      },
      "& .MuiStepLabel-label.Mui-active": {
        color: "#0052CC",
      },
      "& .MuiTypography-caption": {
        fontSize: "0.875rem",
      },
    },
  };

  return (
    <>
      <Box
        display="flex"
        flexDirection="column"
        alignItems="flex-start"
        sx={classes.header}
      >
        <Typography variant="h6">Record History</Typography>
        <Typography variant="caption">
          All history information about this record
        </Typography>
      </Box>

      <Stepper orientation="vertical" sx={classes.container}>
        {historySteps.map((step, index) => (
          <Step key={step.label} sx={classes.step}>
            <StepLabel
              optional={
                index === 1 ? (
                  <Typography variant="caption">{step.description}</Typography>
                ) : index === 2 ? (
                  <Typography variant="caption">{step.description}</Typography>
                ) : null
              }
            >
              {step.label}
            </StepLabel>
            <StepContent>
              <Typography variant="caption">{step.description}</Typography>
              <Box sx={{ mb: 2 }}></Box>
            </StepContent>
          </Step>
        ))}
      </Stepper>
    </>
  );
};

export default HistoryStepper;
