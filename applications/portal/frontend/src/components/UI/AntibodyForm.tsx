import React from "react";
import { makeStyles } from "@mui/styles";
import { vars } from "../../theme/variables";
import {
  Box,
  Container,
  TextField,
  Paper,
  Grid,
  Typography,
  useTheme,
  Toolbar,
  Button,
  Backdrop,
  CircularProgress,
} from "@mui/material";
import DoneIcon from "@mui/icons-material/Done";

import { useFormik } from "formik";

import Input from "./Input";
import FormLine from "./FormLine";

const { bannerHeadingColor, backgroundColorForm } = vars;

const useStyles = makeStyles((theme?: any) => ({
  container: { padding: theme.spacing(10) },
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
}));

const AntibodyForm = (props) => {
  const { initialValues, validationSchema, onSubmit, title } = props;
  const classes = useStyles();
  const theme = useTheme();
  const classesToolbar = {
    toolbar: {
      position: "fixed",
      bottom: 0,
      left: 0,
      minWidth: "100vw",
      backgroundColor: theme.palette.common.white,
      boxShadow:
        "0px -20px 24px -4px rgba(16, 24, 40, 0.02), 0px -8px 8px -4px rgba(16, 24, 40, 0.03)",
    },
    content: {
      display: "flex",
      justifyContent: "flex-end",
    },
  };

  const formik = useFormik({
    enableReinitialize: true,
    initialValues: initialValues,
    validationSchema: validationSchema,
    onSubmit,
    validateOnChange: true,
    validateOnBlur: true,
  });

  const { handleSubmit } = formik;

  return (
    <form
      onSubmit={handleSubmit}
      autoComplete="off"
      style={{ background: backgroundColorForm }}
    >
      {formik.isSubmitting && <Backdrop sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }} open={true} ><CircularProgress color="primary" /></Backdrop>}
      <Container maxWidth="xl" className={classes.container}>
        <Paper className={classes.paper}>
          <Grid
            container
            direction="column"
            gap={3}
            m={0}
            width="100%"
            height="100%"
          >
            <Grid item>
              <Typography variant="h1" className={classes.header}>
                {title}
              </Typography>
            </Grid>
            <Grid item className={classes.formItem}>
              <FormLine>
                <Box>
                  <Input
                    name="catalogNumber"
                    label="Identifier"
                    required={false}
                    readOnly={true}
                    formik={formik}
                    placeholder="An catalogNumber unique to your antibody (e.g. Labname_001 or myab_1023)"
                  />
                </Box>
                <Box>
                  <Input
                    name="vendor"
                    label="Principal Investigator - Institution or Vendor"
                    required={false}
                    readOnly={true}
                    formik={formik}
                    placeholder="(e.g. J. Doe - Harvard)"
                  />
                </Box>
              </FormLine>
            </Grid>
            <Grid item className={classes.formItem}>
              <FormLine>
                <Box>
                  <Input
                    name="url"
                    label="Principal Investigator's/Institution's Website or Vendor Website"
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
            <Grid item className={classes.formItem}>
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
            <Grid item className={classes.formItem}>
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
            <Grid item className={classes.formItem}>
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
            <Grid item className={classes.formItem}>
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
            <Grid item className={classes.formItem}>
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
            <Grid item>
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
            <Grid item>
              <Typography variant="h5" className={classes.label}>
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
              />
            </Grid>
          </Grid>
        </Paper>
      </Container>
      <Toolbar sx={classesToolbar.toolbar}>
        <Container maxWidth="xl">
          <Box sx={classesToolbar.content}>
            <Button
              variant="contained"
              color="primary"
              startIcon={<DoneIcon fontSize="small" />}

              type="submit"
              disabled={
                formik && (!(formik.isValid && formik.dirty) || formik.isSubmitting )
              }
            >
              Submit
            </Button>
          </Box>
        </Container>
      </Toolbar>
    </form>
  );
};

export default AntibodyForm;
