import { Link } from "@mui/material";
import React from "react";
import { useHistory, useLocation } from "react-router-dom";

interface LinkButtonProps {
  label?: string;
  href?: string;
  onClick?: (e: any) => any;
  className?: string;
}

const LinkButton = (props: LinkButtonProps) => {
  return (
    <Link
      component="button"
      underline="none"
      variant="body2"
      sx={(theme) => ({
        fontWeight: 500,
        color: theme.palette.grey[700],
        px: theme.spacing(1.5),
        py: theme.spacing(1),
        "&.selected": {
          bgcolor: theme.palette.grey[100],
          borderRadius: theme.shape.borderRadius,
          color: theme.palette.grey[900],
        },
      })}
      {...props}
    >
      {props.label}
    </Link>
  );
};

const NavLinks = () => {
  const history = useHistory();
  const location = useLocation();

  const isHomeViewActive =
    location.pathname == "/" || location.pathname == "/submissions";
  const isAboutViewActive = location.pathname == "/about";

  return (
    <>
      <LinkButton
        className={isHomeViewActive ? "selected" : ""}
        label="Home"
        onClick={() => history.push("/")}
      />
      <LinkButton
        className={isAboutViewActive ? "selected" : ""}
        label="About"
        onClick={() => history.push("/about")}
      />
    </>
  );
};

export default NavLinks;
