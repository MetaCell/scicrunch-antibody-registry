import React from "react";

import { vars } from "../../theme/variables";
import {
  Box,
  Container,
  TextField,
  Paper,
  Typography,
  InputAdornment,
  Select,
  MenuItem,
} from "@mui/material";
import Grid from "@mui/material/Grid2"
import { AlertIcon } from "../icons";

import StepNavigation from "./StepNavigation";
import { useFormik } from "formik";
import * as yup from "yup";
import { postNewAntibody } from "../../helpers/antibody";
import { validateCatalogNumber } from "../../utils/antibody";

const { bannerHeadingColor, primaryTextColor } = vars;

const styles = {
  container: { padding: 10 },
  paper: {
    textAlign: "start",
    border: "1px solid #EAECF0",
    borderRadius: "1rem",
    boxShadow:
      " 0px 12px 16px -4px rgba(16, 24, 40, 0.08), 0px 4px 6px -2px rgba(16, 24, 40, 0.03)",
    padding: "3rem",
  },
  formItem: {
    display: "flex",
    alignItems: "center",
    "& .MuiInputBase-root.MuiOutlinedInput-root": {
      boxShadow: "0px 1px 2px rgba(16, 24, 40, 0.05)",
    },
  },
  header: {
    color: bannerHeadingColor,
    paddingTop: 0,
  },
  label: {
    color: bannerHeadingColor,
    marginBottom: "0.375rem",
  },
  note: {
    color: primaryTextColor,
    fontWeight: 400,
  },
};

const requiredFieldValidation = yup.string().required("The field is mandatory");

const validationSchema = yup.object().shape({
  catalogNumber: validateCatalogNumber,
  vendor: requiredFieldValidation,
  name: requiredFieldValidation,
  host: requiredFieldValidation,
  targetSpecies: requiredFieldValidation,
  antibodyTarget: requiredFieldValidation,
  clonality: requiredFieldValidation,
  url: yup
    .string()
    .url("Please enter a valid URL that starts with http or https")
    .required("This field is mandatory"),
});

const Input = ({ formik, label, name, required, placeholder }) => {
  const { errors, touched, getFieldProps, values, handleChange } = formik;

  return (<>
    <Typography variant="h5" sx={styles.label}>
      {label} {required && "(Mandatory)"}
    </Typography>
    {name === "clonality" ? (
      <Select
        name="clonality"
        value={formik.values.clonality}
        onChange={formik.handleChange}
        fullWidth
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
          name={name}
          placeholder={placeholder}
          value={values[name]}
          onChange={handleChange}
          {...getFieldProps(name)}
          error={Boolean(touched[name] && errors[name])}
          helperText={touched[name] && errors[name]}
          slotProps={{
            input: {
              endAdornment: (
                <InputAdornment position="end">
                  {touched[name] && errors[name] && <AlertIcon />}
                </InputAdornment>
              ),
            }
          }}
        />
        {!touched[name] && !errors[name] && name === "catalogNumber" && (
          <Typography variant="subtitle1" sx={styles.note}>
            Note: Submit unregistered antibodies only
          </Typography>
        )}
      </>
    )}
  </>);
};

const FormLine = ({ children }) => {
  const child = React.Children.toArray(children);
  return (
    <Grid container spacing={3}>
      <Grid size={{ lg: 6 }}>
        {child[0]}
      </Grid>
      <Grid size={{ lg: 6 }}>
        {child[1]}
      </Grid>
    </Grid>
  );
};
const PersonalForm = (props) => {

  const { setAntibodyId, setApiResponse, next } = props;

  const postAntibody = (antibody) => {
    let ab = { ...antibody, type: "personal" };
    postNewAntibody(ab, setAntibodyId, setApiResponse, next);
  };

  const formik = useFormik({
    enableReinitialize: true,
    initialValues: {
      catalogNumber: "",
      vendor: "",
      url: "",
      name: "",
      host: "",
      targetSpecies: "",
      antibodyTarget: "",
      clonality: "unknown",
      cloneID: "",
      isotype: "",
      conjugate: "",
      format: "",
      uniprotID: "",
      epitope: "",
      applications: "",
      citation: "",
      comments: "",
    },
    validationSchema: validationSchema,
    onSubmit: (values) => {
      postAntibody(values);
    },
    validateOnChange: true,
    validateOnBlur: true,
  });

  const { handleSubmit } = formik;

  return (
    (<form onSubmit={handleSubmit} autoComplete="off" className="antibody-form type-personal">
      <Container maxWidth="xl" sx={styles.container}>
        <Paper sx={styles.paper}>
          <Grid
            container
            direction="column"
            sx={{
              gap: 3,
              m: 0,
              width: "100%",
              height: "100%"
            }}>
            <Grid>
              <Typography variant="h1" sx={styles.header} className="title-antibody-details">
                2. Antibody Details
              </Typography>
            </Grid>
            <Grid sx={styles.formItem}>
              <FormLine>
                <Box>
                  <Input
                    name="catalogNumber"
                    label="Identifier"
                    required={true}
                    formik={formik}
                    placeholder="An catalogNumber unique to your antibody (e.g. Labname_001 or myab_1023)"
                  />
                </Box>
                <Box>
                  <Input
                    name="vendor"
                    label="Principal Investigator/Institution"
                    required={true}
                    formik={formik}
                    placeholder="(e.g. J. Doe - Harvard)"
                  />
                </Box>
              </FormLine>
            </Grid>
            <Grid sx={styles.formItem}>
              <FormLine>
                <Box>
                  <Input
                    name="url"
                    label="Principal Investigator's/Institution's Website"
                    required={true}
                    formik={formik}
                    placeholder="http:// or https://"
                  />
                </Box>
                <Box>
                  <Input
                    name="name"
                    label="Antibody name"
                    required={true}
                    formik={formik}
                    placeholder="Anti-phospho-Glo1(Y136) Antibody"
                  />
                </Box>
              </FormLine>
            </Grid>
            <Grid sx={styles.formItem}>
              <FormLine>
                <Box>
                  <Input
                    name="host"
                    label="Host Species"
                    required={true}
                    formik={formik}
                    placeholder="Rabbit"
                  />
                </Box>
                <Box>
                  <Input
                    name="targetSpecies"
                    label="Target/Reactive Species"
                    required={true}
                    formik={formik}
                    placeholder="Mouse"
                  />
                </Box>
              </FormLine>
            </Grid>
            <Grid sx={styles.formItem}>
              <FormLine>
                <Box>
                  <Input
                    name="antibodyTarget"
                    label="Antibody Target"
                    required={true}
                    formik={formik}
                    placeholder="phospho-Glo1(Y136)"
                  />
                </Box>
                <Box>
                  <Input
                    name="clonality"
                    label="Clonality"
                    required={true}
                    formik={formik}
                    placeholder="Polyclonal"
                  />
                </Box>
              </FormLine>
            </Grid>
            <Grid sx={styles.formItem}>
              <FormLine>
                <Box>
                  <Input
                    name="cloneID"
                    label="Clone ID"
                    required={false}
                    formik={formik}
                    placeholder="C200234"
                  />
                </Box>
                <Box>
                  <Input
                    name="isotype"
                    label="Isotype"
                    required={false}
                    formik={formik}
                    placeholder="IgG"
                  />
                </Box>
              </FormLine>
            </Grid>
            <Grid sx={styles.formItem}>
              <FormLine>
                <Box>
                  <Input
                    name="conjugate"
                    label="Conjugate"
                    required={false}
                    formik={formik}
                    placeholder="Alexa Fluor 488"
                  />
                </Box>
                <Box>
                  <Input
                    name="format"
                    label="Antibody Form/Format"
                    required={false}
                    formik={formik}
                    placeholder="glycerol-free"
                  />
                </Box>
              </FormLine>
            </Grid>
            <Grid sx={styles.formItem}>
              <FormLine>
                <Box>
                  <Input
                    name="uniprotID"
                    label="Uniprot ID"
                    required={false}
                    formik={formik}
                    placeholder="Q13255"
                  />
                </Box>
                <Box>
                  <Input
                    name="epitope"
                    label="Epitope"
                    required={false}
                    formik={formik}
                    placeholder="IAVPDV(phosphoY)SA(homoalanine)KRFC"
                  />
                </Box>
              </FormLine>
            </Grid>
            <Grid>
              <FormLine>
                <Box>
                  <Input
                    name="applications"
                    label="Applications"
                    required={false}
                    formik={formik}
                    placeholder="WB"
                  />
                </Box>
                <Box>
                  <Input
                    name="citation"
                    label="Defining Citation"
                    required={false}
                    formik={formik}
                    placeholder="PMID of paper describing production of antibody"
                  />
                </Box>
              </FormLine>
            </Grid>
            <Grid>
              <Typography variant="h5" sx={styles.label}>
                Comments
              </Typography>
              <TextField
                fullWidth
                name="comments"
                multiline
                rows={5}
                placeholder="Antibody was produced by ... [Insert procedure]"
                value={formik.values.comments}
                onChange={formik.handleChange}
                className="input-comments"
              />
            </Grid>
          </Grid>
        </Paper>
      </Container>
      <StepNavigation
        previous={props.previous}
        next={next}
        hasPrevious={props.hasPrevious}
        isLastStep={true}
        activeStep={2}
        formik={formik}
      />
    </form>)
  );
};

export default PersonalForm;
