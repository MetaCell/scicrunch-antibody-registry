import React, { useState } from "react";
import { Box } from "@mui/material";

interface MultiStepProps {
  children: React.ReactNode;
}

const MultiStep = (props: MultiStepProps) => {
  const { children } = props;
  const [stepNumber, setStepNumber] = useState(0);

  const steps = React.Children.toArray(children) as React.ReactElement[];
  const step = steps[stepNumber];

  const next = () => {
    setStepNumber(stepNumber + 1);
  };

  const previous = () => {
    setStepNumber(stepNumber - 1);
  };

  const stepProps = {
    previous,
    next,
    hasPrevious: stepNumber > 0,
  };

  const stepWithProps = React.cloneElement(step, { ...stepProps });

  return <Box sx={{ height: "100%" }} className="step">{stepWithProps}</Box>;
};

export default MultiStep;
