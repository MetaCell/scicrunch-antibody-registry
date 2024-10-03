import React from "react";
import {
  AppBar,
  Box,
  Container,
  Toolbar,
  Link,
  Stack,
  Typography,
  Grid
} from "@mui/material";
import FooterLinks from "./FooterLinks";


const Footer = () => {

  return (
    (<Box
      sx={{
        width: 1,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0.75rem 7.5rem',
        borderTop: '1px solid #EAECF0',
        background: '#fff',
        marginTop: 'auto'
      }}>
      <Stack direction="row" spacing={2} sx={{
        alignItems: "center"
      }}>
        <Link className="logo" href="/">
          <img src={"/assets/footer-logo.svg"} title="Antibody Registry" alt="Antibody Registry Logo" />
        </Link>
        <Typography variant="body2" align="center">
          Have any questions? Contact us at {" "}
          <Link
            target="_blank"
            href="mailto:rii-help@scicrunch.org"
            className="link-contact-us"
            sx={{
              textDecoration: 'underline'
            }}
          >
            rii-help@scicrunch.org
          </Link>
        </Typography>
      </Stack>
      <Stack direction="row" spacing={3} sx={{
        alignItems: "center"
      }}>
        <FooterLinks />
      </Stack>
    </Box>)
  );
};

export default Footer;
