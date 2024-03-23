import { Button, Link } from "@mui/material";
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
    <Button
      component={Link}
      className="link-button"
      underline="none"
      href={props.href}
      sx={(theme) => ({
        fontWeight: 600,
        color: theme.palette.grey[500],
        "&:hover": {
          color: theme.palette.grey[600],
        },
      })}
      {...props}
    >
      {props.label}
    </Button>
  );
};

const LINKS = [{ label: "Contact Us", href: ["/contact-us"] }, { label: "Become a member", href: ["/membership"] }, { label: "Terms & Conditions", href:  ["/terms-and-conditions"] }];

const FooterLinks = () => {
  const history = useHistory();
  const location = useLocation();

  return (
    <>
      {LINKS.map((link) => (
        <LinkButton key={link.label}
          className={link.href.includes(location.pathname) ? "selected" : ""}
          label={link.label}
          href={link.href[0]}
          onClick={(e) => { e.preventDefault(); history.push(link.href[0])}}
        />
      ))} 
    </>
  );
};

export default FooterLinks;
