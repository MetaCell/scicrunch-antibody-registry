import { Link } from "@mui/material";
import React, { useState } from "react";
import { useHistory } from 'react-router-dom';

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
  const [isHomeViewActive, setIsHomeViewActive] = useState(true);
  const [isAboutViewActive, setIsAboutViewActive] = useState(false);
  const history = useHistory();
  const handleOnClick = (e) => {
    if (e.target.innerText === "Home") {
      setIsHomeViewActive(true);
      setIsAboutViewActive(false);
      history.push('/');
    } else {
      setIsHomeViewActive(false);
      setIsAboutViewActive(true);
      history.push('/about');
    }
  };


  return (
    <>
      <LinkButton
        className={isHomeViewActive ? "selected" : ""}
        label="Home"
        // href="/"
        onClick={handleOnClick}
      />
      <LinkButton
        className={isAboutViewActive ? "selected" : ""}
        label="About"
        // href="/about"
        onClick={handleOnClick}
      />
    </>
  );
};

export default NavLinks;
