import React from "react";
import { Container, Stack, Typography, Button, Box } from "@mui/material";
import { useTheme } from "@mui/system";
import { CircleCheckIcon } from "../icons";

const SuccessSubmission = (props) => {
  const theme = useTheme();
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
        <Typography variant="h1">Antibody successfully submitted</Typography>
        <Typography variant="subtitle1" align="center" sx={classes.message}>
          Your antibody submission was successfully received. A member of our
          curators team will review it as soon as possible ans approve or deny
          it. Its apparition in the public registry can take up several days due
          to manual curation.
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
