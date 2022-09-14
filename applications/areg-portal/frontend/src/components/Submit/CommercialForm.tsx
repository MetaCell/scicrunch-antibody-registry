import React from "react";
import { makeStyles } from "@mui/styles";
import { vars } from "../../theme/variables";
import {
  TextField,
  Paper,
  Grid,
  Typography,
  InputAdornment,
} from "@mui/material";
import { AlertIcon } from "../icons";

import StepNavigation from "./StepNavigation";
import { useFormik } from "formik";
import * as yup from "yup";
const { bannerHeadingColor, primaryTextColor } = vars;

const useStyles = makeStyles((theme?: any) => ({
  paper: {
    textAlign: "start",
    border: "1px solid #EAECF0",
    borderRadius: "1rem",
    boxShadow:
      " 0px 12px 16px -4px rgba(16, 24, 40, 0.08), 0px 4px 6px -2px rgba(16, 24, 40, 0.03)",
    padding: "3rem",
    width: "720px",
  },
  formItem: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    "& .MuiInputBase-root.MuiOutlinedInput-root": {
      height: "2.5rem",
      boxShadow: "0px 1px 2px rgba(16, 24, 40, 0.05)",
      width: "300px",
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
}));

const validationSchema = yup.object().shape({
  catalogNumber: yup.string().required("The field is mandatory"),
});

const CommercialForm = (props) => {
  const classes = useStyles();

  const formik = useFormik({
    enableReinitialize: true,
    initialValues: {
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
      alert(JSON.stringify(values, null, 2));
    },
    validateOnChange: true,
  });

  const { errors, touched, handleSubmit, isSubmitting, getFieldProps } = formik;

  return (
    <form onSubmit={handleSubmit}>
      <Paper className={classes.paper}>
        <Grid container direction="column" gap={3} m={0} width="100%">
          <Grid item>
            <Typography variant="h1" className={classes.header}>
              3/3: Antibody Details
            </Typography>
          </Grid>
          <Grid item>
            <Typography variant="h5" className={classes.label}>
              Catalog Number (Mandatory)
            </Typography>
            <TextField
              fullWidth
              className="antibody-detail-catalogNumber"
              name="catalogNumber"
              value={formik.values.catalogNumber}
              onChange={formik.handleChange}
              {...getFieldProps("catalogNumber")}
              error={Boolean(touched.catalogNumber && errors.catalogNumber)}
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
              fullWidth
              className="antibody-detail-vendor"
              name="vendor"
              placeholder="Cell Signaling Technology"
              value={formik.values.vendor}
              onChange={formik.handleChange}
            />
          </Grid>
          <Grid item className={classes.formItem}>
            <div>
              <Typography variant="h5" className={classes.label}>
                Antibody Name
              </Typography>
              <TextField
                className="antibody-detail-name"
                name="name"
                placeholder="NeuN (D4G4O) XP® Rabbit mAb"
                value={formik.values.name}
                onChange={formik.handleChange}
              />
            </div>
            <div>
              <Typography variant="h5" className={classes.label}>
                Host Species
              </Typography>
              <TextField
                className="antibody-detail-hostSpecies"
                name="host"
                placeholder="Rabbit"
                value={formik.values.host}
                onChange={formik.handleChange}
              />
            </div>
          </Grid>
          <Grid item className={classes.formItem}>
            <div>
              <Typography variant="h5" className={classes.label}>
                Target/Reactive Species
              </Typography>
              <TextField
                className="antibody-detail-targetORreactiveSpecies"
                name="targetSpecies"
                placeholder="Human, Mouse, Rat"
                value={formik.values.targetSpecies}
                onChange={formik.handleChange}
              />
            </div>
            <div>
              <Typography variant="h5" className={classes.label}>
                Antibody Target
              </Typography>
              <TextField
                className="antibody-detail-target"
                name="antibodyTarget"
                placeholder="NeuN"
                value={formik.values.antibodyTarget}
                onChange={formik.handleChange}
              />
            </div>
          </Grid>
          <Grid item className={classes.formItem}>
            <div>
              <Typography variant="h5" className={classes.label}>
                Clonality
              </Typography>
              <TextField
                className="antibody-detail-clonality"
                name="clonality"
                placeholder="Monoclonal"
                value={formik.values.clonality}
                onChange={formik.handleChange}
              />
            </div>
            <div>
              <Typography variant="h5" className={classes.label}>
                Clone ID
              </Typography>
              <TextField
                className="antibody-detail-cloneID"
                name="cloneID"
                placeholder="Clone D4G4O"
                value={formik.values.cloneID}
                onChange={formik.handleChange}
              />
            </div>
          </Grid>
          <Grid item className={classes.formItem}>
            <div>
              <Typography variant="h5" className={classes.label}>
                Isotype
              </Typography>
              <TextField
                className="antibody-detail-isotype"
                name="isotype"
                placeholder="IgG"
                value={formik.values.isotype}
                onChange={formik.handleChange}
              />
            </div>
            <div>
              <Typography variant="h5" className={classes.label}>
                Conjugate
              </Typography>
              <TextField
                className="antibody-detail-conjugate"
                name="conjugate"
                placeholder="Alexa Fluor 488"
                value={formik.values.conjugate}
                onChange={formik.handleChange}
              />
            </div>
          </Grid>
          <Grid item className={classes.formItem}>
            <div>
              <Typography variant="h5" className={classes.label}>
                Antibody Form/Format
              </Typography>
              <TextField
                className="antibody-detail-formORformat"
                name="format"
                placeholder="Azide free"
                value={formik.values.format}
                onChange={formik.handleChange}
              />
            </div>
            <div>
              <Typography variant="h5" className={classes.label}>
                Uniprot ID
              </Typography>
              <TextField
                className="antibody-detail-uniprotID"
                name="uniprotID"
                placeholder="A6NFN3"
                value={formik.values.uniprotID}
                onChange={formik.handleChange}
              />
            </div>
          </Grid>
          <Grid item className={classes.formItem}>
            <div>
              <Typography variant="h5" className={classes.label}>
                Epitope
              </Typography>
              <TextField
                className="antibody-detail-epitope"
                name="epitope"
                placeholder="OTTHUMP00000018992"
                value={formik.values.epitope}
                onChange={formik.handleChange}
              />
            </div>
            <div>
              <Typography variant="h5" className={classes.label}>
                Applications
              </Typography>
              <TextField
                className="antibody-detail-applications"
                name="applications"
                placeholder="ELISA, IHC, WB"
                value={formik.values.applications}
                onChange={formik.handleChange}
              />
            </div>
          </Grid>
          <Grid item>
            <Typography variant="h5" className={classes.label}>
              Comments
            </Typography>
            <TextField
              fullWidth
              className="antibody-detail-comments"
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
      <StepNavigation
        previous={props.previous}
        isLastStep={props.isLastStep}
        next={props.next}
        hasPrevious={props.hasPrevious}
      />
    </form>
  );
};

export default CommercialForm;
