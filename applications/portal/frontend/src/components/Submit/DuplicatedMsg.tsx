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
import { CircleAlertIcon, SearchIcon } from "../icons";
import { useTheme } from "@mui/system";

const DuplicatedMsg = (props) => {
  const theme = useTheme();
  const classes = {
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
      mb: theme.spacing(5),
    },
    label: { color: "grey.700", fontWeight: 500, textAlign: "left" },
    buttonGrey: {
      color: "grey.700",
      padding: theme.spacing(1, 2),
    },
    input: {
      flexGrow: 2,
      display: "flex",
      alignItems: "center",
      padding: theme.spacing(0, 1),
      borderRight: "solid 1px",
      borderColor: theme.palette.grey[300],
      "& .MuiTypography-root": {
        fontSize: "1rem",
        fontWeight: 400,
        color: "grey.900",
      },
    },
    group: {
      border: "solid 1px",
      borderColor: theme.palette.grey[300],
      borderRadius: theme.shape,
    },
    button: {
      width: "fit-content",
    },
  };

  return (
    <Container maxWidth="xl" sx={classes.container}>
      <Box />
      <Stack direction="column" spacing={3} sx={classes.stack}>
        <Box>
          <CircleAlertIcon />
        </Box>
        <Typography variant="h1" color="error.main">
          This antibody is a duplicate
        </Typography>
        {/* <Box>
          <Typography variant="subtitle1" sx={classes.label}>
            Search the antibody by catalog number and save time
          </Typography>
          <Box display="flex" sx={classes.group}>
            <Box sx={classes.input}>
              <Typography>{props.antibodyId}</Typography>
            </Box>
            <Button
              variant="text"
              color="info"
              size="small"
              startIcon={<SearchIcon stroke="black" />}
              sx={classes.buttonGrey}
            >
              Search
            </Button>
          </Box>
        </Box> */}
        <Divider>
          <Typography variant="subtitle1" sx={classes.message}>
            English
          </Typography>
        </Divider>
        <Typography variant="subtitle1" align="center" sx={classes.message}>
          The Antibody you Entered is a Duplicate, which will be Rejected. We
          have found that the antibody you entered already exists in our system.
          The ID associated with the antibody is RRID:AB_
          {props.antibodyId}.
        </Typography>
        <Divider>
          <Typography variant="subtitle1" sx={classes.message}>
            Chinese
          </Typography>
        </Divider>
        <Typography variant="subtitle1" align="center" sx={classes.message}>
          您所提交的抗体已经存在于我们的系统中，此次申请将会被拒绝
          我们发现您所提交的抗体已经存在于我们的系统中，它的ID 是 RRID:AB_
          {props.antibodyId}.
        </Typography>
        <Box>
          <Button
            //onClick={props.onClose}
            href={`/AB_${props.antibodyId}`}
            variant="contained"
            color="primary"
            sx={classes.button}
          >
            Go to the existing antibody record
          </Button>
        </Box>
      </Stack>
      <Link
        target="_blank"
        href="mailto:abr-help@scicrunch.org"
        sx={classes.link}
      >
        Need help? Contact us
      </Link>
    </Container>
  );
};

export default DuplicatedMsg;
