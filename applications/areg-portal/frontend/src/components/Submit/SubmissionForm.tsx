import React from "react";

import {
  Box,
  Button,
  Container,
  Dialog,
  TextField,
  Toolbar,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { useTheme } from "@mui/system";

import MultiStepForm, { FormStep } from "../UI/MultiStepForm";
import AbTypeStep from "./AbTypeStep";

const initialValues = {
  commercialType: "commercial",
  abUrl: "",
  catNum: "",
};

const SubmissionForm = (props) => {
  const theme = useTheme();
  const classes = {
    header: {
      display: "flex",
      justifyContent: "space-between",
      backgroundColor: theme.palette.common.white,
    },
  };
  return (
    <Dialog
      fullScreen
      open={props.open}
      onClose={props.handleClose}
      PaperProps={{
        style: {
          backgroundColor: theme.palette.grey[50],
        },
      }}
    >
      <Box sx={classes.header}>
        <Container maxWidth="xl">
          <Toolbar sx={classes.header}>
            <Button
              onClick={props.handleClose}
              variant="contained"
              color="info"
              startIcon={<CloseIcon fontSize="small" />}
            >
              Close
            </Button>
            <Box
              component="img"
              src="./assets/logo.svg"
              title="Antibody Registry"
              justifySelf="center"
            />
            <Button
              startIcon={<CloseIcon fontSize="small" />}
              variant="contained"
              color="info"
              sx={{ visibility: "hidden" }}
            >
              Close
            </Button>
          </Toolbar>
        </Container>
      </Box>
      <Container maxWidth="xl">
        <MultiStepForm
          initialValues={initialValues}
          onSubmit={(values) => {
            alert(JSON.stringify(values, null, 2));
          }}
        >
          <FormStep
            stepName="commercialType"
            onSubmit={() => console.log("step 1")}
          >
            <AbTypeStep label="Type of Antibody" name="commercialType" />
          </FormStep>
          <FormStep stepName="abUrl" onSubmit={() => console.log("step 2")}>
            <TextField fullWidth id="url " label="URL" name="abUrl" />
          </FormStep>
        </MultiStepForm>
      </Container>
    </Dialog>
  );
};

export default SubmissionForm;
