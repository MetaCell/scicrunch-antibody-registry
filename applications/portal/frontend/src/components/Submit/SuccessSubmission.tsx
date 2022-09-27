import React from "react";
import { Container, Stack, Typography, Button, Box, Link } from "@mui/material";
import { CircleCheckIcon } from "../icons";

const SuccessSubmission = (props) => {
  const classes = {
    container: {
      height: "100%",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
    },
    stack: {
      display: "flex",
      justifyContent: "center",
      "& .MuiSvgIcon-fontSizeMedium": {
        fontSize: "3rem",
      },
    },
    message: {
      color: "grey.500",
      maxWidth: "560px",
    },
    button: {
      width: "fit-content",
    },
  };

  return (
    <Container maxWidth="xl" sx={classes.container}>
      <Stack direction="column" spacing={3} sx={classes.stack}>
        <Box>
          <CircleCheckIcon />
        </Box>
        <Typography variant="h1">Successfully Added your Antibody</Typography>
        <Typography variant="subtitle1" align="center" sx={classes.message}>
          Your antibody has been successfully submitted to the Antibody
          Registry. You should receive an email response from{" "}
          <Link target="_blank" href="mailto:curation@scicrunch.com">
            curation@scicrunch.com
          </Link>{" "}
          in 1 business day with your antibody's official RRID. If approved, the
          data will be publicly available at{" "}
          <Link target="_blank" href="https://www.antibodyregistry.org">
            antibodyregistry.org
          </Link>{" "}
          in approximately 8 business days.
          <br /> If you have any questions feel free to contact us at{" "}
          <Link target="_blank" href="mailto:abr-help@scicrunch.org">
            abr-help@scicrunch.org
          </Link>
          <br />
          Your temporary ID is RRID: AB_{props.temporaryID}
        </Typography>
        <Box>
          <Button
            onClick={props.onClose}
            variant="contained"
            color="primary"
            sx={classes.button}
          >
            See my submission
          </Button>
        </Box>
      </Stack>
    </Container>
  );
};

export default SuccessSubmission;
