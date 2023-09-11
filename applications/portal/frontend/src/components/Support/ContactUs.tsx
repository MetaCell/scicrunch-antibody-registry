import React from "react";

import SupportTabs from "../UI/SupportTabs";
import { Link, Container, Typography } from "@mui/material";

const ContactUs = () => {
  const styles = {

    message: {
      color: "grey.500",
      maxWidth: "480px",
      fontSize:'1rem',
      fontWeight:600
    },
    container:{ display:'flex', justifyContent:'center' }
  }
  
  return (
    <SupportTabs>
      <Container maxWidth='xl' sx={styles.container} className="container-contact-us">
     
        <Typography variant="subtitle1" align="center" sx={styles.message}>
Have any questions? Please feel free to{" "}
          <Link
            target="_blank"
            href="https://www.scicrunch.com/contact"
            className="link-contact-us"
          >
      contact us
          </Link>
        </Typography>
   
      </Container>
    </SupportTabs>
  )
}

export default ContactUs;