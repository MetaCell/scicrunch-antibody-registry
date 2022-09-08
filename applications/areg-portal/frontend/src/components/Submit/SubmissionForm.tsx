import React from "react";
import { Formik } from "formik";

import { Button, Dialog, TextField } from "@mui/material";

const initialValues = {
  abType: "",
  abUrl: "",
  catNum: "",
};

const SubmissionForm = (props) => {
  return (
    <Dialog fullScreen open={props.open} onClose={props.handleClose}>
      <Formik
        initialValues={initialValues}
        onSubmit={(values) => {
          alert(JSON.stringify(values, null, 2));
        }}
      >
        {(formik) => (
          <form onSubmit={formik.handleSubmit}>
            <TextField
              fullWidth
              id="abType"
              name="abType"
              label="Type of Antibody"
              value={formik.values.abType}
              onChange={formik.handleChange}
            />
            <Button type="submit">Submit</Button>
            <Button onClick={props.handleClose}>Close</Button>
          </form>
        )}
      </Formik>
    </Dialog>
  );
};

export default SubmissionForm;
