import React from "react";

import { Button, Dialog, TextField } from "@mui/material";

import MultiStepForm, { FormStep } from "../UI/MultiStepForm";
import AbTypeStep from "./AbTypeStep";

const initialValues = {
  commercialType: "commercial",
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
        <FormStep
          stepName="commercialType"
          onSubmit={() => console.log("step 1")}
        >
          <AbTypeStep label="Type of Antibody" name="commercialType" />
        </FormStep>
        <FormStep stepName="abUrl" onSubmit={() => console.log("step 2")}>
          <TextField fullWidth id="url " label="URL" name="abUrl" />
        </FormStep>
      </MultiStepForm>
      <Button onClick={props.handleClose}>Close</Button>
    </Dialog>
  );
};

export default SubmissionForm;
