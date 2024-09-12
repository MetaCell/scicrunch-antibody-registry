import React from 'react'

import { Box, Button, Container,Typography } from '@mui/material';
import SupportTabs from '../UI/SupportTabs';


const InquirePage = () => {
  
  return (
    (<SupportTabs>
      <Container maxWidth="lg" sx={{ display: 'flex', alignItems: "center", flexDirection: "column" }} className="container-inquire">
        <Typography component="p">
      For companies that would like to be members of the Antibody Registry, there are benefits to membership and there are steps that will need to be taken. 

A few slides explain these:
        </Typography>
        <Box sx={{
          my: 3
        }}>
          <iframe src="https://www.slideshare.net/slideshow/embed_code/key/7ty1jMcsosffdG?hostedIn=slideshare&page=upload" width="952" height="586" frameBorder="0" marginWidth="0" marginHeight="0" scrolling="no"></iframe>
        </Box>
        <Box >
          <Typography component="h2" variant='h2' >
Benefits of membership
          </Typography>
          <ul>
            <li>Help your customers comply with journal and funder mandates</li>
            <li>Improve discoverability of your antibodies</li>
            <li>Find out who is working with your products</li>
          </ul>

So get on the right side of reproducibility; stop being the problem, be the solution!
          <Typography component="p" >
contact <a href="mailto:rii-help@scicrunch.org">rii-help@scicrunch.org</a> to become a member today.

          </Typography>
        </Box>
      </Container>
    </SupportTabs>)
  );
}

export default InquirePage;