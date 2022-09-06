import { Box, Container } from "@mui/material";
import React from "react";
import { makeStyles } from "@mui/styles";
import { vars } from "../../theme/variables";

import Header from "../UI/Header";

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

const useStyles = makeStyles(() => ({}));

export const AntibodyDetail = () => {
  const classes = useStyles();
  return <Header>Antibody detail</Header>;
};

export default AntibodyDetail;
