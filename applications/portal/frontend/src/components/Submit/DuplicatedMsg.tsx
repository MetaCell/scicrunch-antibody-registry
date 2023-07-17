import React from "react";
import {
  Container,
  Stack,
  Typography,
  Button,
  Box,
  Link,
  Divider,
} from "@mui/material";
import { CircleAlertIcon } from "../icons";

const styles = {
  container: {
    minHeight: "90vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "space-between",
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
    maxWidth: "480px",
  },
  link: {
    color: "primary.dark",
    fontSize: "1rem",
    fontWeight: 600,
    mb: 5,
  },
  button: {
    width: "fit-content",
  },
};

const DuplicatedMsg = (props) => { 

  return (
    <Container maxWidth="xl" sx={styles.container} className="container-duplicate">
      <Box />
      <Stack direction="column" spacing={3} sx={styles.stack}>
        <Box>
          <CircleAlertIcon />
        </Box>
        <Typography variant="h1" color="error.light" className="duplicate-message">
          This antibody is a duplicate
        </Typography>
        <Divider>
          <Typography variant="subtitle1" sx={styles.message}>
            English
          </Typography>
        </Divider>
        <Typography variant="subtitle1" component="p" align="center" sx={styles.message} className="english-message">
          The Antibody you Entered is a Duplicate, which will be Rejected. We
          have found that the antibody you entered already exists in our system.
          The ID associated with the antibody is 
          
        </Typography>
        <Typography variant="subtitle1" align="center" sx={{ ...styles.message, fontWeight: 700, fontSize: "1em" }}>
          RRID:AB_{props.antibodyId}.
        </Typography>
        <Divider>
          <Typography variant="subtitle1" sx={styles.message}>
            Chinese
          </Typography>
        </Divider>
        <Typography variant="subtitle1" component="p" align="center" sx={styles.message} className="chinese-message">
          此次申请将会被拒绝，因为我们发现您所提交的抗体已经存在于我们的系统中，它的ID是
        </Typography>
        <Typography variant="subtitle1" align="center" sx={{ ...styles.message, fontWeight: 700, fontSize: "1em" }}>
          RRID:AB_{props.antibodyId}.
        </Typography>
        <Box>
          <Button
            href={`/AB_${props.antibodyId}`}
            variant="contained"
            color="primary"
            sx={styles.button}
            className="btn-go-to-antibody"
          >
            Go to the existing antibody record
          </Button>
        </Box>
      </Stack>
      <Link
        target="_blank"
        href="mailto:abr-help@scicrunch.org"
        sx={styles.link}
        className="link-contact"
      >
        Need help? Contact us
      </Link>
    </Container>
  );
};

export default DuplicatedMsg;
