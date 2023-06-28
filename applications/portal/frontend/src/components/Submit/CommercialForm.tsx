import React, { useState } from "react";
import { makeStyles } from "@mui/styles";
import { vars } from "../../theme/variables";
import {
  Box,
  Container,
  TextField,
  Paper,
  Grid,
  Typography,
  InputAdornment,
  Divider,
  CardMedia,
  Select,
  MenuItem,
} from "@mui/material";
import { AlertIcon } from "../icons";

import StepNavigation from "./StepNavigation";
import { useFormik } from "formik";
import * as yup from "yup";
import { postNewAntibody } from "../../helpers/antibody";

const {
  bannerHeadingColor,
  primaryTextColor,
  backgroundColorForm,
  contentBorderColor,
} = vars;

const styles = {
  background: {
    background: {
      lg: `linear-gradient(90deg, ${contentBorderColor} 50%, ${backgroundColorForm} 50%)`,
      xs: contentBorderColor
    }
  },
  rightContainer: (theme) => ({
    padding: { 
      lg: theme.spacing(10, 0, 10, 10),
      xs: 0,
    },
    pr: 0,
    height: "90vh",
    overflow: "auto",
    "&::-webkit-scrollbar": {
      display: "none",
    },
  }),
  leftContainer: (theme) => ({
    padding: { 
      lg: theme.spacing(10, 0, 10, 10),
      xs: 0,
    },
  }),
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
  leftBox: (theme) => ({
    padding: theme.spacing(6, 0, 3, 0),
    textAlign: "start",
    height: "100%",
  }),
  iframeDefault: (theme) => ({
    height: "100%",
    minHeight: "320px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: theme.palette.grey[700],
    border: `0.25rem solid ${contentBorderColor}`,
    borderRadius: theme.shape.borderRadius,
  }),
};

const validationSchema = yup.object().shape({
  catalogNumber: yup.string().required("The field is mandatory"),
  url: yup
    .string()
    .url("Please enter a valid URL that starts with http or https")
    .required("This field is mandatory"),
});

const Iframe = ({ formik }) => {
  const { errors, touched, getFieldProps } = formik;


  return (
    <Box sx={styles.leftBox}>
      <Grid
        container
        direction="column"
        gap={3}
        m={0}
        width="100%"
        height="100%"
        wrap="nowrap"
      >
        <Grid item>
          <Typography variant="h1" sx={styles.header}>
            2. Product Page Link
          </Typography>
        </Grid>
        <Grid item>
          <Typography variant="h5" sx={styles.label}>
            Vendor Product Page Link (Mandatory)
          </Typography>
          <TextField
            fullWidth
            name="url"
            value={formik.values.url}
            onChange={formik.handleChange}
            {...getFieldProps("url")}
            error={Boolean(touched.url && errors.url)}
            helperText={touched.url && errors.url}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  {touched.url && errors.url && <AlertIcon />}
                </InputAdornment>
              ),
              style: {
                backgroundColor: "white",
              },
            }}
          />
          {!touched.catalogNumber && !errors.catalogNumber && (
            <Typography variant="subtitle1" sx={styles.note}>
              Enter a link to the product's page on the vendor's website
            </Typography>
          )}
        </Grid>
        <Divider sx={{ my: 1 }} />
        <Grid item lg={8}>
          {touched.url && !errors.url ? (
            <CardMedia
              sx={styles.iframeDefault}
              component="iframe"
              src={formik.values.url}
            />
          ) : (
            <Box sx={styles.iframeDefault}>
              <Typography variant="subtitle1" sx={{ color: "grey.400" }}>
                Enter a link in the field above to get a preview of the website
              </Typography>
            </Box>
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

const FormLine = ({ children }) => {
  const child = React.Children.toArray(children) as React.ReactElement[];
  return (
    <Grid container spacing={3}>
      <Grid item lg={6}>
        {child[0]}
      </Grid>
      <Grid item lg={6}>
        {child[1]}
      </Grid>
    </Grid>
  );
};
const CommercialForm = (props) => {

  const { setAntibodyId, setApiResponse, next } = props;

  const postAntibody = (antibody) => {
    let ab = { ...antibody, type: "commercial" };
    postNewAntibody(ab, setAntibodyId, setApiResponse, next);
  };

  const formik = useFormik({
    enableReinitialize: true,
    initialValues: {
      url: "",
      catalogNumber: "",
      vendor: "",
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
      comments: "",
    },
    validationSchema: validationSchema,
    onSubmit: (values) => {
      postAntibody(values);
    },
    validateOnChange: true,
    validateOnBlur: true,
  });

  const { errors, touched, handleSubmit, getFieldProps } = formik;

  return (
    <Box component="form"
      onSubmit={handleSubmit}
      sx={styles.background}
      autoComplete="off"
      className="antibody-form type-commercial"
    >
      <Container maxWidth="xl">
        <Grid container>
          <Grid item lg={6} sx={styles.leftContainer}>
            <Iframe formik={formik} />
          </Grid>
          <Grid item lg={6} sx={styles.rightContainer} >
            <Paper sx={styles.paper}>
              <Grid container direction="column" gap={3} m={0} width="100%">
                <Grid item>
                  <Typography variant="h1" sx={styles.header}>
                    3. Antibody Details
                  </Typography>
                </Grid>
                <Grid item>
                  <Typography variant="h5" sx={styles.label}>
                    Catalog Number (Mandatory)
                  </Typography>
                  <TextField
                    fullWidth
                    className="antibody-detail-catalogNumber"
                    name="catalogNumber"
                    value={formik.values.catalogNumber}
                    onChange={formik.handleChange}
                    {...getFieldProps("catalogNumber")}
                    error={Boolean(
                      touched.catalogNumber && errors.catalogNumber
                    )}
                    helperText={touched.catalogNumber && errors.catalogNumber}
                    InputProps={{
                      endAdornment: (
                        <InputAdornment position="end">
                          {touched.catalogNumber && errors.catalogNumber && (
                            <AlertIcon />
                          )}
                        </InputAdornment>
                      ),
                    }}
                  />
                  {!touched.catalogNumber && !errors.catalogNumber && (
                    <Typography variant="subtitle1" sx={styles.note}>
                      Note: Submit unregistered antibodies only
                    </Typography>
                  )}
                </Grid>
                <Grid item>
                  <Typography variant="h5" sx={styles.label}>
                    Vendor
                  </Typography>
                  <TextField
                    fullWidth
                    className="antibody-detail-vendor"
                    name="vendor"
                    placeholder="Cell Signaling Technology"
                    value={formik.values.vendor}
                    onChange={formik.handleChange}
                  />
                </Grid>
                <Grid item sx={styles.formItem}>
                  <FormLine>
                    <Box>
                      <Typography variant="h5" sx={styles.label}>
                        Antibody Name
                      </Typography>
                      <TextField
                        fullWidth
                        className="antibody-detail-name"
                        name="name"
                        placeholder="NeuN (D4G4O) XP® Rabbit mAb"
                        value={formik.values.name}
                        onChange={formik.handleChange}
                      />
                    </Box>
                    <Box>
                      <Typography variant="h5" sx={styles.label}>
                        Host Species
                      </Typography>
                      <TextField
                        className="antibody-detail-hostSpecies"
                        name="host"
                        placeholder="Rabbit"
                        value={formik.values.host}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                  </FormLine>
                </Grid>
                <Grid item sx={styles.formItem}>
                  <FormLine>
                    <Box>
                      <Typography variant="h5" sx={styles.label}>
                        Target/Reactive Species
                      </Typography>
                      <TextField
                        name="targetSpecies"
                        placeholder="Human, Mouse, Rat"
                        value={formik.values.targetSpecies}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                    <Box>
                      <Typography variant="h5" sx={styles.label}>
                        Antibody Target
                      </Typography>
                      <TextField
                        name="antibodyTarget"
                        placeholder="NeuN"
                        value={formik.values.antibodyTarget}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                  </FormLine>
                </Grid>
                <Grid item sx={styles.formItem}>
                  <FormLine>
                    <Box>
                      <Typography variant="h5" sx={styles.label}>
                        Clonality
                      </Typography>

                      <Select
                        name="clonality"
                        value={formik.values.clonality}
                        onChange={formik.handleChange}
                        fullWidth
                      >
                        <MenuItem value={"unknown"}>Unknown</MenuItem>
                        <MenuItem value={"cocktail"}>Cocktail</MenuItem>
                        <MenuItem value={"control"}>Control</MenuItem>
                        <MenuItem value={"isotype control"}>
                          Isotype Control
                        </MenuItem>
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
                    </Box>
                    <Box>
                      <Typography variant="h5" sx={styles.label}>
                        Clone ID
                      </Typography>
                      <TextField
                        name="cloneID"
                        placeholder="Clone D4G4O"
                        value={formik.values.cloneID}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                  </FormLine>
                </Grid>
                <Grid item sx={styles.formItem}>
                  <FormLine>
                    <Box>
                      <Typography variant="h5" sx={styles.label}>
                        Isotype
                      </Typography>
                      <TextField
                        name="isotype"
                        placeholder="IgG"
                        value={formik.values.isotype}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                    <Box>
                      <Typography variant="h5" sx={styles.label}>
                        Conjugate
                      </Typography>
                      <TextField
                        name="conjugate"
                        placeholder="Alexa Fluor 488"
                        value={formik.values.conjugate}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                  </FormLine>
                </Grid>
                <Grid item sx={styles.formItem}>
                  <FormLine>
                    <Box>
                      <Typography variant="h5" sx={styles.label}>
                        Antibody Form/Format
                      </Typography>
                      <TextField
                        name="format"
                        placeholder="Azide free"
                        value={formik.values.format}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                    <Box>
                      <Typography variant="h5" sx={styles.label}>
                        Uniprot ID
                      </Typography>
                      <TextField
                        name="uniprotID"
                        placeholder="A6NFN3"
                        value={formik.values.uniprotID}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                  </FormLine>
                </Grid>
                <Grid item sx={styles.formItem}>
                  <FormLine>
                    <Box>
                      <Typography variant="h5" sx={styles.label}>
                        Epitope
                      </Typography>
                      <TextField
                        name="epitope"
                        placeholder="OTTHUMP00000018992"
                        value={formik.values.epitope}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                    <Box>
                      <Typography variant="h5" sx={styles.label}>
                        Applications
                      </Typography>
                      <TextField
                        name="applications"
                        placeholder="ELISA, IHC, WB"
                        value={formik.values.applications}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                  </FormLine>
                </Grid>
                <Grid item>
                  <Typography variant="h5" sx={styles.label}>
                    Comments
                  </Typography>
                  <TextField
                    fullWidth
                    name="comments"
                    multiline
                    rows={5}
                    placeholder="Anything we should know about this antibody?"
                    value={formik.values.comments}
                    onChange={formik.handleChange}
                  />
                </Grid>
              </Grid>
            </Paper>
          </Grid>
        </Grid>
      </Container>
      <StepNavigation
        previous={props.previous}
        next={next}
        hasPrevious={props.hasPrevious}
        isLastStep={true}
        activeStep={2}
        formik={formik}
      />
    </Box>
  );
};

export default CommercialForm;
