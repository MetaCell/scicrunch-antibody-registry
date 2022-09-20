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
} from "@mui/material";
import { AlertIcon } from "../icons";

import StepNavigation from "./StepNavigation";
import { useFormik } from "formik";
import * as yup from "yup";

const { bannerHeadingColor, primaryTextColor } = vars;

const useStyles = makeStyles((theme?: any) => ({
  background: {
    background: `linear-gradient(90deg, ${theme.palette.grey[100]} 50%, ${theme.palette.grey[50]} 50%)`,
    [theme.breakpoints.down("lg")]: {
      background: theme.palette.grey[100],
    },
  },
  rightContainer: {
    padding: theme.spacing(10, 0, 10, 10),
    [theme.breakpoints.down("lg")]: {
      padding: 0,
    },
    height: "90vh",
    overflow: "auto",
    "&::-webkit-scrollbar": {
      display: "none",
    },
  },
  leftContainer: {
    padding: theme.spacing(10, 10, 10, 0),
    [theme.breakpoints.down("lg")]: {
      padding: 0,
    },
  },
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
  leftBox: {
    padding: theme.spacing(6, 0, 3, 0),
    textAlign: "start",
    height: "100%",
  },
  iframeDefault: {
    height: "100%",
    minHeight: "320px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: theme.palette.grey[700],
    border: `0.25rem solid ${theme.palette.grey[100]}`,
    borderRadius: theme.shape.borderRadius,
  },
}));

const validationSchema = yup.object().shape({
  catalogNumber: yup.string().required("The field is mandatory"),
  url: yup
    .string()
    .url("Please enter a valid URL that starts with http or https")
    .required("This field is mandatory"),
});

const Iframe = ({ formik, handleBlur }) => {
  const { errors, touched, getFieldProps } = formik;
  const classes = useStyles();

  return (
    <Box className={classes.leftBox}>
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
          <Typography variant="h1" className={classes.header}>
            2. Product Page Link
          </Typography>
        </Grid>
        <Grid item>
          <Typography variant="h5" className={classes.label}>
            Vendor Product Page Link (Mandatory)
          </Typography>
          <TextField
            fullWidth
            name="url"
            value={formik.values.url}
            onChange={formik.handleChange}
            onBlur={handleBlur}
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
            <Typography variant="subtitle1" className={classes.note}>
              Enter a link to the product's page on the vendor's website
            </Typography>
          )}
        </Grid>
        <Divider sx={{ my: 1 }} />
        <Grid item lg={8}>
          {touched.url && !errors.url ? (
            <CardMedia
              className={classes.iframeDefault}
              component="iframe"
              src={formik.values.url}
            />
          ) : (
            <Box className={classes.iframeDefault}>
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
  const classes = useStyles();

  const [isLastStep, setIsLastStep] = useState(false);
  const [isUrlEntered, setIsUrlEntered] = useState(false);

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
      clonality: "",
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
      console.log(values);
      props.next();
    },
    validateOnChange: true,
    validateOnBlur: true,
  });

  const { errors, touched, handleSubmit, getFieldProps, setFieldTouched } =
    formik;

  const handleNext = (e) => {
    e.preventDefault();

    if (touched.url && !errors.url) {
      setIsUrlEntered(true);
      setIsLastStep(true);
    }
    if (!touched.url) {
      setFieldTouched("url", true);
    }
  };

  const handleBlur = (e) => {
    try {
      new URL(e.target.value);
      setIsUrlEntered(true);
      setIsLastStep(true);
    } catch {}
  };

  return (
    <form
      onSubmit={handleSubmit}
      className={classes.background}
      autoComplete="off"
      onBlur={handleBlur}
    >
      <Container maxWidth="xl">
        <Grid container>
          <Grid item lg={6} className={classes.leftContainer}>
            <Iframe formik={formik} handleBlur={handleBlur} />
          </Grid>
          <Grid item lg={6} className={classes.rightContainer} sx={{ pr: 0 }}>
            <Paper className={classes.paper}>
              <Grid container direction="column" gap={3} m={0} width="100%">
                <Grid item>
                  <Typography variant="h1" className={classes.header}>
                    3. Antibody Details
                  </Typography>
                </Grid>
                <Grid item>
                  <Typography variant="h5" className={classes.label}>
                    Catalog Number (Mandatory)
                  </Typography>
                  <TextField
                    fullWidth
                    disabled={!isUrlEntered}
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
                    <Typography variant="subtitle1" className={classes.note}>
                      Note: Submit unregistered antibodies only
                    </Typography>
                  )}
                </Grid>
                <Grid item>
                  <Typography variant="h5" className={classes.label}>
                    Vendor
                  </Typography>
                  <TextField
                    disabled={!isUrlEntered}
                    fullWidth
                    className="antibody-detail-vendor"
                    name="vendor"
                    placeholder="Cell Signaling Technology"
                    value={formik.values.vendor}
                    onChange={formik.handleChange}
                  />
                </Grid>
                <Grid item className={classes.formItem}>
                  <FormLine>
                    <Box>
                      <Typography variant="h5" className={classes.label}>
                        Antibody Name
                      </Typography>
                      <TextField
                        disabled={!isUrlEntered}
                        fullWidth
                        className="antibody-detail-name"
                        name="name"
                        placeholder="NeuN (D4G4O) XP® Rabbit mAb"
                        value={formik.values.name}
                        onChange={formik.handleChange}
                      />
                    </Box>
                    <Box>
                      <Typography variant="h5" className={classes.label}>
                        Host Species
                      </Typography>
                      <TextField
                        disabled={!isUrlEntered}
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
                <Grid item className={classes.formItem}>
                  <FormLine>
                    <Box>
                      <Typography variant="h5" className={classes.label}>
                        Target/Reactive Species
                      </Typography>
                      <TextField
                        disabled={!isUrlEntered}
                        name="targetSpecies"
                        placeholder="Human, Mouse, Rat"
                        value={formik.values.targetSpecies}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                    <Box>
                      <Typography variant="h5" className={classes.label}>
                        Antibody Target
                      </Typography>
                      <TextField
                        disabled={!isUrlEntered}
                        name="antibodyTarget"
                        placeholder="NeuN"
                        value={formik.values.antibodyTarget}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                  </FormLine>
                </Grid>
                <Grid item className={classes.formItem}>
                  <FormLine>
                    <Box>
                      <Typography variant="h5" className={classes.label}>
                        Clonality
                      </Typography>
                      <TextField
                        disabled={!isUrlEntered}
                        name="clonality"
                        placeholder="Monoclonal"
                        value={formik.values.clonality}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                    <Box>
                      <Typography variant="h5" className={classes.label}>
                        Clone ID
                      </Typography>
                      <TextField
                        disabled={!isUrlEntered}
                        name="cloneID"
                        placeholder="Clone D4G4O"
                        value={formik.values.cloneID}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                  </FormLine>
                </Grid>
                <Grid item className={classes.formItem}>
                  <FormLine>
                    <Box>
                      <Typography variant="h5" className={classes.label}>
                        Isotype
                      </Typography>
                      <TextField
                        disabled={!isUrlEntered}
                        name="isotype"
                        placeholder="IgG"
                        value={formik.values.isotype}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                    <Box>
                      <Typography variant="h5" className={classes.label}>
                        Conjugate
                      </Typography>
                      <TextField
                        disabled={!isUrlEntered}
                        name="conjugate"
                        placeholder="Alexa Fluor 488"
                        value={formik.values.conjugate}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                  </FormLine>
                </Grid>
                <Grid item className={classes.formItem}>
                  <FormLine>
                    <Box>
                      <Typography variant="h5" className={classes.label}>
                        Antibody Form/Format
                      </Typography>
                      <TextField
                        disabled={!isUrlEntered}
                        name="format"
                        placeholder="Azide free"
                        value={formik.values.format}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                    <Box>
                      <Typography variant="h5" className={classes.label}>
                        Uniprot ID
                      </Typography>
                      <TextField
                        disabled={!isUrlEntered}
                        name="uniprotID"
                        placeholder="A6NFN3"
                        value={formik.values.uniprotID}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                  </FormLine>
                </Grid>
                <Grid item className={classes.formItem}>
                  <FormLine>
                    <Box>
                      <Typography variant="h5" className={classes.label}>
                        Epitope
                      </Typography>
                      <TextField
                        disabled={!isUrlEntered}
                        name="epitope"
                        placeholder="OTTHUMP00000018992"
                        value={formik.values.epitope}
                        onChange={formik.handleChange}
                        fullWidth
                      />
                    </Box>
                    <Box>
                      <Typography variant="h5" className={classes.label}>
                        Applications
                      </Typography>
                      <TextField
                        disabled={!isUrlEntered}
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
                  <Typography variant="h5" className={classes.label}>
                    Comments
                  </Typography>
                  <TextField
                    fullWidth
                    disabled={!isUrlEntered}
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
        next={handleNext}
        hasPrevious={props.hasPrevious}
        isLastStep={isLastStep}
        activeStep={isLastStep ? 2 : 1}
        totalSteps={3}
      />
    </form>
  );
};

export default CommercialForm;