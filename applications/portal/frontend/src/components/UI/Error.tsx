import React from "react";
import { Container, Typography, Button, Stack, Box } from "@mui/material";

const Error = (props) => {
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
    (<Container maxWidth="xl" sx={classes.container} className="error-container">
      <Stack spacing={3} sx={classes.stack}>
        <Typography variant="h1" sx={{
          color: "grey.700"
        }}>
          Something went wrong
        </Typography>
        <Typography variant="subtitle1" align="center" sx={classes.message}>
          Error message: {props.detail}. We are sorry for the inconvenience
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
export default Error;