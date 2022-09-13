import React, { useState } from "react";

import { Box, Button, Container, Dialog, Toolbar } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { useTheme } from "@mui/system";

import MultiStep, { Step } from "../UI/MultiStep";
import AbTypeStep from "./AbTypeStep";
import CommercialForm from "./CommercialForm";

const SubmissionForm = (props) => {
  const theme = useTheme();
  const classes = {
    header: {
      display: "flex",
      justifyContent: "space-between",
      backgroundColor: theme.palette.common.white,
    },
  };

  const [selectedType, setSelectedType] = useState("commercial");

  const handleTypeSelector = (value: string) => {
    setSelectedType(value);
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
        <MultiStep>
          <Step
            stepName="commercialType"
            onNext={() => console.log(selectedType)}
          >
            <AbTypeStep
              label="Type of Antibody"
              name="commercialType"
              selectedValue={selectedType}
              handleChange={(e) => handleTypeSelector(e)}
            />
          </Step>
          <Step stepName="catNum" onNext={() => console.log("step 2")}>
            {selectedType === "commercial" ? (
              <CommercialForm />
            ) : (
              <Box> soy el paso 2</Box>
            )}
          </Step>
        </MultiStep>
      </Container>
    </Dialog>
  );
};

export default SubmissionForm;
