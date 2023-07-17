import React from "react";
import { Container, Stack, Typography, Button, Box, Link } from "@mui/material";
import { CircleCheckIcon } from "../icons";

const styles = {
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

const SuccessSubmission = (props) => {
  

  return (
    <Container maxWidth="xl" sx={styles.container} className="container-success-submission">
      <Stack direction="column" spacing={3} sx={styles.stack}>
        <Box>
          <CircleCheckIcon />
        </Box>
        <Typography variant="h1" className="title">Successfully Added your Antibody</Typography>
        <Typography variant="subtitle1" align="center" sx={styles.message}>
          Your antibody has been successfully submitted to the Antibody
          Registry. You should receive an email response from{" "}
          <Link className="link-contact-curation" target="_blank" href="mailto:curation@scicrunch.com">
            curation@scicrunch.com
          </Link>{" "}
          in 1 business day with your antibody&apos;s official RRID. If approved, the
          data will be publicly available at{" "}
          <Link className="link-home" href="/">
            antibodyregistry.org
          </Link>{" "}
          in approximately 8 business days.
          <br /> If you have any questions feel free to contact us at{" "}
          <Link className="link-contact" target="_blank" href="mailto:abr-help@scicrunch.org">
            abr-help@scicrunch.org
          </Link>
          <br />
          Your temporary ID is
        </Typography>
        <Typography className="temporary-id" variant="h5" align="center">
          RRID: AB_{props.temporaryID}
        </Typography>
        <Box>
          <Button
            onClick={() => (window.location.href = "/submissions")}
            variant="contained"
            color="primary"
            sx={styles.button}
            className="btn-go-to-submissions"
          >
            See my submissions
          </Button>
        </Box>
      </Stack>
    </Container>
  );
};

export default SuccessSubmission;
