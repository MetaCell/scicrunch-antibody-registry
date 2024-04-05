import { Button, Link } from "@mui/material";
import React from "react";
import { useHistory, useLocation } from "react-router-dom";
import { UserContext } from "../../services/UserService";

interface LinkButtonProps {
  label?: string;
  href?: string;
  onClick?: (e: any) => any;
  className?: string;
}

const LinkButton = (props: LinkButtonProps) => {
  return (
    <Button
      component={Link}
      className="link-button"
      underline="none"

      href={props.href}
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
    </Button>
  );
};

const LINKS = [{ label: "Home", href: ["/", "/submissions"] }, { label: "About", href: ["/about"] }, { label: "FAQ", href:  ["/faq"] }];

const NavLinks = () => {
  const history = useHistory();
  const location = useLocation();
  const user = React.useContext(UserContext)[0];

  return (
    <>
      {LINKS.map((link) => (
        <LinkButton key={link.label}
          className={link.href.includes(location.pathname) ? "selected" : ""}
          label={link.label}
          href={link.href[0]}
          onClick={(e) => {e.preventDefault(); history.push(link.href[0])}}
        />
      ))} 
      {
        user && 
        <LinkButton
          className={"download" ==  location.pathname ? "selected" : ""}
          label={"Download"}
          href={"/download"}
          onClick={(e) => {e.preventDefault(); history.push("/download")}}
        />
      }
    </>
  );
};

export default NavLinks;
