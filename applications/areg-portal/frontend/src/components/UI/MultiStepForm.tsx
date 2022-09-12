import React, { useState } from "react";
import {
  Formik,
  Form,
  FormikConfig,
  FormikHelpers,
  FormikValues,
} from "formik";
import { Box, Button, Container, Stack, Toolbar } from "@mui/material";
import { useTheme } from "@mui/system";

interface MultiStepFormProps extends FormikConfig<FormikValues> {
  children: React.ReactNode;
}

interface FormNavigationProps {
  hasPrevious?: Boolean;
  onBackClick: (values: FormikValues) => void;
  isLastStep: Boolean;
}

const FormNavigation = (props: FormNavigationProps) => {
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
            >
              Previous
            </Button>

            <Button type="submit" variant="contained" color="primary">
              {props.isLastStep ? "Submit" : "Next"}
            </Button>
          </Stack>
        </Box>
      </Container>
    </Toolbar>
  );
};

const MultiStepForm = (props: MultiStepFormProps) => {
  const { children, initialValues, onSubmit } = props;
  const [stepNumber, setStepNumber] = useState(0);
  const [snapshot, setSnapshot] = useState(initialValues);

  const steps = React.Children.toArray(children) as React.ReactElement[];
  const step = steps[stepNumber];
  const totalSteps = steps.length;
  const isLastStep = stepNumber === totalSteps - 1;

  const next = (values: FormikValues) => {
    setSnapshot(values);
    setStepNumber(stepNumber + 1);
  };

  const previous = (values: FormikValues) => {
    setSnapshot(values);
    setStepNumber(stepNumber - 1);
  };

  const handleSubmit = (
    values: FormikValues,
    actions: FormikHelpers<FormikValues>
  ) => {
    // if the step has its own submit function run it first
    if (step.props.onSubmit) {
      step.props.onSubmit(values);
    }

    // in the last step run the parent onSubmit function (MultiStepForm onSubmit prop)
    //otherwise reset the touched obj so the validation doesn't fire while navigating back and forth
    // and go to next step
    if (isLastStep) {
      return onSubmit(values, actions);
    } else {
      actions.setTouched({});
      next(values);
    }
  };

  return (
    <Formik initialValues={initialValues} onSubmit={handleSubmit}>
      {(formik) => (
        <Form>
          {step}
          <FormNavigation
            isLastStep={isLastStep}
            hasPrevious={stepNumber > 0}
            onBackClick={() => previous(formik.values)}
          />
        </Form>
      )}
    </Formik>
  );
};

export default MultiStepForm;

export const FormStep = ({ stepName = "", children }: any) => children;
