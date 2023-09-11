import React from "react";
import Typography from "@mui/material/Typography";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import { AlertIcon } from "../icons";

import { vars } from "../../theme/variables";

const { bannerHeadingColor, primaryTextColor } = vars;

const styles = {
  label: {
    color: bannerHeadingColor,
    marginBottom: "0.375rem",
  },
  note: {
    color: primaryTextColor,
    fontWeight: 400,
  },
};

const Input = ({
  formik,
  label,
  name,
  required,
  placeholder,
  readOnly = false,
}) => {
  const { errors, touched, getFieldProps, values, handleChange } = formik;

  return (
    <>
      <Typography variant="h5" sx={styles.label}>
        {label} {required && "(Mandatory)"}
      </Typography>
      {name === "clonality" ? (
        <Select
          name="clonality"
          value={formik.values.clonality}
          onChange={formik.handleChange}
          fullWidth
          className="clonality-select"
        >
          <MenuItem value={"unknown"}>Unknown</MenuItem>
          <MenuItem value={"cocktail"}>Cocktail</MenuItem>
          <MenuItem value={"control"}>Control</MenuItem>
          <MenuItem value={"isotype control"}>Isotype Control</MenuItem>
          <MenuItem value={"monoclonal"}>Monoclonal</MenuItem>
          <MenuItem value={"monoclonal secondary"}>
            Monoclonal Secondary
          </MenuItem>
          <MenuItem value={"polyclonal"}>Polyclonal</MenuItem>
          <MenuItem value={"polyclonal secondary"}>
            Polyclonal Secondary
          </MenuItem>
          <MenuItem value={"oligoclonal"}>Oligoclonal</MenuItem>
          <MenuItem value={"recombinant"}>Recombinant</MenuItem>
          <MenuItem value={"recombinant monoclonal"}>
            Recombinant Monoclonal
          </MenuItem>
          <MenuItem value={"recombinant monoclonal secondary"}>
            Recombinant Monoclonal Secondary
          </MenuItem>
          <MenuItem value={"recombinant polyclonal"}>
            Recombinant Polyclonal
          </MenuItem>
          <MenuItem value={"recombinant polyclonal secondary"}>
            Recombinant Polyclonal Secondary
          </MenuItem>
        </Select>
      ) : (
        <>
          <TextField
            fullWidth
            disabled={readOnly}
            name={name}
            placeholder={placeholder}
            value={values[name]}
            onChange={handleChange}
            {...getFieldProps(name)}
            error={Boolean(touched[name] && errors[name])}
            helperText={touched[name] && errors[name]}
            className={`input-${name}`}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  {touched[name] && errors[name] && <AlertIcon />}
                </InputAdornment>
              ),
            }}
          />
        </>
      )}
    </>
  );
};

export default Input;
