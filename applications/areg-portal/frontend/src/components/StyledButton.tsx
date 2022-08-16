import React from "react";
import { Button, ButtonProps } from "@mui/material";
import { styled, darken } from "@mui/material/styles";

interface StyledButtonProps extends ButtonProps {
  bgPrimary?: boolean;
}

const CustomizedButton = styled(Button, {
  shouldForwardProp: (prop) => prop !== "bgPrimary",
})<StyledButtonProps>(({ bgPrimary, theme }) => ({
  borderRadius: "0.375rem",
  fontWeight: 600,
  padding: `${theme.spacing(0.6)} ${theme.spacing(2)}`,
  color: bgPrimary ? theme.palette.common.white : theme.palette.grey[700],
  backgroundColor: bgPrimary
    ? theme.palette.primary.main
    : theme.palette.common.white,
  border: !bgPrimary && `1px solid ${theme.palette.grey[300]}`,
  boxShadow:
    "0px 1px 2px rgba(16, 24, 40, 0.05)" +
    (bgPrimary ? ",inset 0px -2px 0px rgba(0, 0, 0, 0.25)" : ""),
  "&:hover": {
    backgroundColor: bgPrimary && darken(theme.palette.primary.main, 0.2),
  },
  "&.Mui-disabled": {
    color: !bgPrimary && theme.palette.grey[300],
    borderColor: !bgPrimary && theme.palette.grey[200],
  },
}));

const StyledButton = (props) => {
  return (
    <CustomizedButton bgPrimary={props.bgPrimary} disabled={props.disabled}>
      {props.children}
    </CustomizedButton>
  );
};

export default StyledButton;
