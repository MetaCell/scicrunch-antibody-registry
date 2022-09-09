import React from "react";

import { Button, Dialog } from "@mui/material";

import MultiStepForm, { FormStep } from "../UI/MultiStepForm";
import AbTypeStep from "./AbTypeStep";

const initialValues = {
  abType: "",
  abUrl: "",
  catNum: "",
};

const SubmissionForm = (props) => {
  return (
    <Dialog fullScreen open={props.open} onClose={props.handleClose}>
      <MultiStepForm
        initialValues={initialValues}
        onSubmit={(values) => {
          alert(JSON.stringify(values, null, 2));
        }}
      >
        <FormStep stepName="abType" onSubmit={() => console.log("step 1")}>
          <AbTypeStep label="Type of Antibody" name="abType" />
        </FormStep>
        <FormStep stepName="abUrl" onSubmit={() => console.log("step 2")}>
          <AbTypeStep label="URL" name="abUrl" />
          <AbTypeStep label="CatNum" name="CatNum" />
        </FormStep>
      </MultiStepForm>
      <Button onClick={props.handleClose}>Close</Button>
    </Dialog>
  );
};

export default SubmissionForm;
