import React from "react";
import { FieldConfig, useField } from "formik";
import { TextField } from "@mui/material";

interface AbTypeStep extends FieldConfig {
  label: string;
}

const AbTypeStep = ({ label, ...props }: AbTypeStep) => {
  const [field, meta] = useField(props);
  return <TextField label={label} {...field} {...props} />;
};

export default AbTypeStep;
