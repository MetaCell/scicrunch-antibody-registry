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
import { Antibody } from "../../rest";



const HistoryStepper = (props: {classes: any, antibody: Antibody}) => {
  let { classes, antibody } = props;
  const theme = useTheme();

  const historySteps = [
    {
      label: new Date(antibody.lastEditTime ?? antibody.curateTime).toLocaleString() + " (current version)",
      description: "Latest update",
    },
    antibody.curateTime && {
      label: new Date(antibody.curateTime).toLocaleString(),
      description: "Antibody approved",
    },
    {
      label: new Date(antibody.insertTime).toLocaleString(),
      description: "Antibody Submitted",
    },
  ];

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
        color: theme.palette.grey[700],
      },
      "& .MuiStepLabel-label.Mui-active": {
        color: theme.palette.primary.dark,
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
        {historySteps.filter(step => step).map((step, index) => (
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
