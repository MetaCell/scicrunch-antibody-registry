import React from "react";
import { FieldConfig, useField, Field } from "formik";
import { InputLabel } from "@mui/material";

interface AbTypeStep extends FieldConfig {
  label: string;
}

const AbTypeStep = ({ label, ...props }: AbTypeStep) => {
  const [field, meta] = useField(props);

  return (
    <>
      <InputLabel>
        <Field type="radio" {...field} {...props} value="commercial" />
        Commercial
      </InputLabel>
      <InputLabel>
        <Field type="radio" {...field} {...props} value="personal" />
        Personal
      </InputLabel>
      <InputLabel>
        <Field type="radio" {...field} {...props} value="other" />
        Other
      </InputLabel>
    </>
  );
};

export default AbTypeStep;
