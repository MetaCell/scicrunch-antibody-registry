import { Container, Typography, Button, Stack, Box } from "@mui/material";
import React from "react";

const Error500 = () => {
  const classes = {
    container: {
      minHeight: "90vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
    },
    stack: {
      display: "flex",
      justifyContent: "center",
    },
    message: {
      color: "grey.500",
      maxWidth: "480px",
    },
  };
  return (
    (<Container maxWidth="xl" sx={classes.container} className="error-container-500">
      <Stack spacing={3} sx={classes.stack}>
        <Typography variant="h1" sx={{
          color: "grey.700"
        }}>
          Internal Server Error
        </Typography>
        <Typography variant="subtitle1" align="center" sx={classes.message}>
          An unexpected error has occurred. We are sorry for the inconvenience, please try again later.
          If the problem persists, please contact us at <pre>abr-help -at- scicrunch -dot- org</pre>.
        </Typography>
        <Box>
          <Button variant="contained" href="/" sx={{ width: "fit-content" }} className="button-return">
            Return to Home Page
          </Button>
        </Box>
      </Stack>
    </Container>)
  );
};
export default Error500;