import React from 'react'

import { Alert, Box, Button, Container,Typography } from '@mui/material';

import SubHeader from "./UI/SubHeader";
import { UserContext } from "../services/UserService";

const DownloadPage = () => {
  const user = React.useContext(UserContext)[0];
  return (<>
    <SubHeader>Downloads</SubHeader>
    {user ? <Container maxWidth="lg"  sx={{ display: 'flex', alignItems: "center", flexDirection: "column", py: 8 }} className="container-download">
      <Button variant="contained" component="a" target="_blank" href="/api/antibodies/export">Download as CSV</Button>
      <Box sx={{
        mt: 4
      }}>
        <Typography component="h2" variant='h2' >
How to cite this data
        </Typography>

        <Typography component="p" sx={{
          my: 2
        }} >
          * Data was downloaded from the antibodyregistry.org, {new Date().toLocaleDateString('en-US', {
            day: '2-digit',
            month: 'long',
            year: 'numeric',
          })} RRID:SCR_006397
        </Typography>
        <Typography component="p" >
          <b>License</b>: CC-0
          <br />
          <b>Note</b>: The data you are downloading is updated weekly

        </Typography>
      </Box>
    </Container> : <Alert severity="info">Please login to download data</Alert>}
  </>);
}

export default DownloadPage;