import React, { useState } from "react";
import { Box, Button, Container, Stack, Toolbar } from "@mui/material";
import { useTheme } from "@mui/system";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import DoneIcon from "@mui/icons-material/Done";

interface MultiStep {
  children: React.ReactNode;
}

const MultiStep = (props: MultiStep) => {
  const { children } = props;
  const [stepNumber, setStepNumber] = useState(0);

  const steps = React.Children.toArray(children) as React.ReactElement[];
  const step = stepNumber === 0 ? steps[stepNumber] : steps[1];
  const totalSteps = steps.length;
  const isLastStep = stepNumber === totalSteps;

  const next = () => {
    setStepNumber(stepNumber + 1);
  };

  const previous = () => {
    setStepNumber(stepNumber - 1);
  };

  const stepProps = {
    previous,
    next,
    isLastStep,
    hasPrevious: stepNumber > 0,
  };

  const stepWithProps = React.cloneElement(step, { ...stepProps });

  return <Box>{stepWithProps}</Box>;
};

export default MultiStep;
