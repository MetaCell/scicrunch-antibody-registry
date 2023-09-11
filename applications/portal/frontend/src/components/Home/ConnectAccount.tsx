import React from "react";
import { Container, Stack, Typography, Button, Box } from "@mui/material";

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

const ConnectAccount = () => {
  

  return (
    <Container maxWidth="xl" sx={styles.container} className="container-create-account">
      <Stack direction="column" spacing={3} sx={styles.stack}>
        <Typography variant="h1">Connect to your account</Typography>
        <Typography variant="subtitle1" align="center" sx={styles.message}>
          Connect to your account to see your submissions.
        </Typography>
        <Box>
          <Button
            onClick={() => (window.location.href = "/login")}
            variant="contained"
            color="primary"
            sx={styles.button}
            className="btn-login"
          >
            Log in / Register
          </Button>
        </Box>
      </Stack>
    </Container>
  );
};

export default ConnectAccount;
