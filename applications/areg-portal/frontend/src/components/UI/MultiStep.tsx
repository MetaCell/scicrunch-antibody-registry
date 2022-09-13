import React, { useState } from "react";
import { Box, Button, Container, Stack, Toolbar } from "@mui/material";
import { useTheme } from "@mui/system";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import DoneIcon from "@mui/icons-material/Done";

interface MultiStep {
  children: React.ReactNode;
}

interface NavigationProps {
  hasPrevious?: Boolean;
  onBackClick: () => void;
  isLastStep: Boolean;
  onNextClick: () => void;
}

const StepNavigation = (props: NavigationProps) => {
  const theme = useTheme();
  const classes = {
    toolbar: {
      position: "fixed",
      bottom: 0,
      left: 0,
      minWidth: "100vw",
      backgroundColor: theme.palette.common.white,
      boxShadow:
        "0px -20px 24px -4px rgba(16, 24, 40, 0.02), 0px -8px 8px -4px rgba(16, 24, 40, 0.03)",
    },
    content: {
      display: "flex",
      justifyContent: "space-between",
    },
  };
  return (
    <Toolbar sx={classes.toolbar}>
      <Container maxWidth="xl">
        <Box sx={classes.content}>
          <Box>Stepper TODO</Box>
          <Stack direction="row" spacing={2}>
            <Button
              disabled={!props.hasPrevious}
              variant="contained"
              color="info"
              onClick={props.onBackClick}
              startIcon={<ChevronLeftIcon fontSize="small" />}
            >
              Previous
            </Button>
            {props.isLastStep ? (
              <Button
                variant="contained"
                color="primary"
                startIcon={<DoneIcon fontSize="small" />}
                type="submit"
                form="add-antibody-form"
              >
                Submit
              </Button>
            ) : (
              <Button
                variant="text"
                color="secondary"
                endIcon={<ChevronRightIcon fontSize="small" />}
                onClick={props.onNextClick}
              >
                Next
              </Button>
            )}
          </Stack>
        </Box>
      </Container>
    </Toolbar>
  );
};

const MultiStep = (props: MultiStep) => {
  const { children } = props;
  const [stepNumber, setStepNumber] = useState(0);

  const steps = React.Children.toArray(children) as React.ReactElement[];
  const step = steps[stepNumber];
  const totalSteps = steps.length;
  const isLastStep = stepNumber === totalSteps - 1;

  const next = () => {
    setStepNumber(stepNumber + 1);
  };

  const previous = () => {
    setStepNumber(stepNumber - 1);
  };

  return (
    <Box>
      {step}
      <StepNavigation
        isLastStep={isLastStep}
        hasPrevious={stepNumber > 0}
        onBackClick={previous}
        onNextClick={next}
      />
    </Box>
  );
};

export default MultiStep;

export const Step = ({ stepName = "", children }: any) => children;
