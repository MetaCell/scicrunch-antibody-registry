import React from "react";
import { Box, Container } from "@mui/material";
import { makeStyles } from "@mui/styles";
import { vars } from "../../theme/variables";

const {
  footerBg,
  whiteColor,
  sepratorColor,
  primaryColor,
  contentBg,
  contentBorderColor,
  primaryTextColor,
  bannerHeadingColor,
} = vars;

const useStyles = makeStyles(() => ({
  banner: {
    background: contentBorderColor,
    paddingTop: "6.3125rem",
    textAlign: "center",
    boxShadow: "inset 0 -7.5rem 7.5rem -5rem rgba(0, 0, 0, 0.1)",
    "& .MuiTypography-root": {
      fontWeight: 600,
      fontSize: "1.875rem",
      lineHeight: "2.375rem",
      color: bannerHeadingColor,
    },
  },
}));

export const Header = (props) => {
  const classes = useStyles();
  return (
    <Box className={classes.banner}>
      <Container maxWidth="xl">
        <Box>{props.children}</Box>
      </Container>
    </Box>
  );
};

export default Header;
