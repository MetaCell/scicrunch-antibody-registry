import React, { useState } from "react";
import { useHistory } from "react-router-dom";

import { Box, Button, Container, Dialog, Toolbar } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { useTheme } from "@mui/system";

import MultiStep from "../UI/MultiStep";
import AbTypeStep from "./AbTypeStep";
import CommercialForm from "./CommercialForm";
import SuccessSubmission from "./SuccessSubmission";
import PersonalForm from "./PersonalForm";
import OtherForm from "./OtherForm";
import DuplicatedMsg from "./DuplicatedMsg";
import Error500 from "../UI/Error500";
import Error from "../UI/Error";

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
  const [antibodyId, setAntibodyId] = useState("");
  const [apiResponse, setApiResponse] = useState({ status: 0, detail: "" });

  const history = useHistory();

  const handleTypeSelector = (value: string) => {
    setSelectedType(value);
  };

  const handleClose = () => {
    history.push("/");
  };

  return (
    <Dialog
      fullScreen
      open={true}
      onClose={handleClose}
      id="dialog-submission-form"
      PaperProps={{
        style: {
          backgroundColor: theme.palette.grey[50],
        },
      }}
    >
      <Box sx={classes.header} className="buttons-container">
        <Container maxWidth="xl">
          <Toolbar sx={classes.header} disableGutters>
            <Button
              onClick={handleClose}
              variant="contained"
              color="info"
              startIcon={<CloseIcon fontSize="small" />}
              className="btn-close btn-close--visible"
            >
              Close
            </Button>
            <Box
              component="img"
              src="./assets/logo.svg"
              title="Antibody Registry"
              justifySelf="center"
              className="logo"
            />
            <Button
              startIcon={<CloseIcon fontSize="small" />}
              onClick={handleClose}
              variant="contained"
              color="info"
              sx={{ visibility: "hidden" }}
              className="btn-close btn-close--hidden"
            >
              Close
            </Button>
          </Toolbar>
        </Container>
      </Box>
      <Box sx={{ height: "100%" }} className="container-steps">
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
              setAntibodyId={setAntibodyId}
              setApiResponse={setApiResponse}
            />
          ) : selectedType === "personal" ? (
            <PersonalForm
              next={props.next}
              previous={props.previous}
              hasPrevious={props.hasPrevious}
              setAntibodyId={setAntibodyId}
              setApiResponse={setApiResponse}
            />
          ) : (
            <OtherForm
              next={props.next}
              previous={props.previous}
              hasPrevious={props.hasPrevious}
              setAntibodyId={setAntibodyId}
              setApiResponse={setApiResponse}
            />
          )}
          {apiResponse.status === 200 ? (
            <SuccessSubmission onClose={handleClose} temporaryID={antibodyId} />
          ) : apiResponse.status === 409 ? (
            <DuplicatedMsg antibodyId={antibodyId} />
          ) : apiResponse.status === 500 ? (
            <Error500 />
          ) : (
            <Error detail={apiResponse.detail} />
          )}
        </MultiStep>
      </Box>
    </Dialog>
  );
};

export default SubmissionForm;
