import React, { useState } from "react";

import { Box, Button, Container, Dialog, Toolbar } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { useTheme } from "@mui/system";

import MultiStep from "../UI/MultiStep";
import AbTypeStep from "./AbTypeStep";
import CommercialForm from "./CommercialForm";
import SuccessSubmission from "./SuccessSubmission";
import PersonalForm from "./PersonalForm";
import OtherForm from "./OtherForm";

const SubmissionForm = (props) => {
  const theme = useTheme();
  const classes = {
    header: {
      position: "sticky",
      top: 0,
      display: "flex",
      justifyContent: "space-between",
      backgroundColor: theme.palette.common.white,
      zIndex: 1,
    },
  };

  const [selectedType, setSelectedType] = useState("commercial");

  const handleTypeSelector = (value: string) => {
    setSelectedType(value);
  };

  const handleClose = () => {
    props.handleClose();
    setSelectedType("commercial");
  };

  return (
    <Dialog
      fullScreen
      open={props.open}
      onClose={handleClose}
      PaperProps={{
        style: {
          backgroundColor: theme.palette.grey[50],
        },
      }}
    >
      <Box sx={classes.header}>
        <Container maxWidth="xl">
          <Toolbar sx={classes.header} disableGutters>
            <Button
              onClick={handleClose}
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
      <Box sx={{ height: "100%" }}>
        <MultiStep>
          <AbTypeStep
            label="Type of Antibody"
            name="commercialType"
            selectedValue={selectedType}
            handleChange={(e) => handleTypeSelector(e)}
            next={props.next}
            previous={props.previous}
            hasPrevious={props.hasPrevious}
          />

          {selectedType === "commercial" ? (
            <CommercialForm
              next={props.next}
              previous={props.previous}
              hasPrevious={props.hasPrevious}
            />
          ) : selectedType === "personal" ? (
            <PersonalForm
              next={props.next}
              previous={props.previous}
              hasPrevious={props.hasPrevious}
            />
          ) : (
            <OtherForm
              next={props.next}
              previous={props.previous}
              hasPrevious={props.hasPrevious}
            />
          )}
          {/* TODO check if the post is sucessfully send correct temporaryID
          If not, add the duplicated message */}
          <SuccessSubmission onClose={handleClose} temporaryID={"AB_2923405"} />
        </MultiStep>
      </Box>
    </Dialog>
  );
};

export default SubmissionForm;
