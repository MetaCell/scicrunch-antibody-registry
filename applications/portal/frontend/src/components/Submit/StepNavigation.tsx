import React from "react";

import { useTheme } from "@mui/system";

import { Button, Toolbar, Container, Box, Stack,  Backdrop,
  CircularProgress, } from "@mui/material";

import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import DoneIcon from "@mui/icons-material/Done";
import Stepper from "./Stepper";

interface NavigationProps {
  hasPrevious?: Boolean;
  previous: () => void;
  next: (e) => void;
  isLastStep?: Boolean;
  activeStep: Number;
  //totalSteps: Number;
  formik?;
}

export const StepNavigation = (props: NavigationProps) => {
  const theme = useTheme();
  const classes = {
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
      justifyContent: "space-between",
    },
  };
  return (
    <>{props.formik?.isSubmitting && <Backdrop sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }} open={true} ><CircularProgress color="primary" /></Backdrop>}
    <Toolbar sx={classes.toolbar}>
      <Container maxWidth="xl">
        <Box sx={classes.content} className="form-steps">
          <Stepper
            activeStep={props.activeStep}
            //totalSteps={props.totalSteps}
          />
          <Stack direction="row" spacing={2}>
            <Button
              disabled={!props.hasPrevious}
              variant="contained"
              color="info"
              onClick={props.previous}
              startIcon={<ChevronLeftIcon fontSize="small" />}
              className="previous-button"
            >
              Previous
            </Button>
            {props.isLastStep ? (
              <Button
                variant="contained"
                color="primary"
                startIcon={<DoneIcon fontSize="small" />}
                type="submit"
                disabled={
                  props.formik && !(props.formik.isValid && props.formik.dirty) || props.formik.isSubmitting
                }
                className="submit-button"
              >
                Submit
              </Button>
            ) : (
              <Button
                variant="text"
                color="secondary"
                endIcon={<ChevronRightIcon fontSize="small" />}
                onClick={(e) => props.next(e)}
                className="next-button"
              >
                Next
              </Button>
            )}
          </Stack>
        </Box>
      </Container>
    </Toolbar>
    </>
  );
};

export default StepNavigation;
