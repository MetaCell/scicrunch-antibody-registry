import React, { useState } from "react";
import {
  Formik,
  Form,
  FormikConfig,
  FormikHelpers,
  FormikValues,
} from "formik";
import { Box, Button } from "@mui/material";

interface MultiStepFormProps extends FormikConfig<FormikValues> {
  children: React.ReactNode;
}

interface FormNavigationProps {
  hasPrevious?: Boolean;
  onBackClick: (values: FormikValues) => void;
  isLastStep: Boolean;
}

const FormNavigation = (props: FormNavigationProps) => {
  return (
    <Box>
      {props.hasPrevious && <Button onClick={props.onBackClick}>Back</Button>}
      <Button type="submit">{props.isLastStep ? "Submit" : "Next"}</Button>
    </Box>
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
    <Formik initialValues={{}} onSubmit={handleSubmit}>
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
