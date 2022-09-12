import React from "react";
import { FieldConfig, useField, Field } from "formik";
import {
  InputLabel,
  Card,
  CardActionArea,
  CardContent,
  Typography,
  Radio,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
} from "@mui/material";

interface AbTypeStep extends FieldConfig {
  label: string;
}

const TypeChoiceCard = ({ children, label }) => {
  return (
    <Card sx={{ maxWidth: 345 }}>
      <CardActionArea>
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {label}
          </Typography>
          {children}
        </CardContent>
      </CardActionArea>
    </Card>
  );
};

const AbTypeStep = ({ label, ...props }: AbTypeStep) => {
  const [field, meta] = useField(props);
  console.log(field);
  console.log(meta);
  console.log(props);

  return (
    <>
      <TypeChoiceCard label="Commercial">
        <Field type="radio" {...field} {...props} value="commercial" />
      </TypeChoiceCard>
      <TypeChoiceCard label="Personal">
        <Field type="radio" {...field} {...props} value="personal" />
      </TypeChoiceCard>
      <TypeChoiceCard label="Other">
        <Field type="radio" {...field} {...props} value="other" />
      </TypeChoiceCard>
    </>
  );
};

export default AbTypeStep;
