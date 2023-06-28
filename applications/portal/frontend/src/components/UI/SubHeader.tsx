import React from "react";
import { Box, Button, Container, Stack, Typography } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { BackIcon } from "../icons";

export const SubHeader = (props) => {
  const theme = useTheme();
  const styles = {
    banner: {
      background: theme.palette.grey[100],
      padding: theme.spacing(10, 0),
      "& .MuiTypography-root": {
        fontWeight: 600,
        fontSize: "1.875rem",
        lineHeight: "2.375rem",
        color: theme.palette.grey[700],
      },
      "& .MuiButtonBase-root": {
        fontWeight: 600,
        fontSize: "1rem",
        color: theme.palette.grey[500],
        padding: 0,
      },
    },
  };
  return (
    <Box sx={styles.banner} className="sub-header">
      <Container maxWidth="xl">
        <Stack spacing={2}>
          <Box>
            <Button
              variant="text"
              onClick={() => (window.location.href = "/")}
              startIcon={<BackIcon />}
              className="button-return"
            >
              Back to Home
            </Button>
          </Box>
          <Typography>{props.children}</Typography>
        </Stack>
      </Container>
    </Box>
  );
};

export default SubHeader;
