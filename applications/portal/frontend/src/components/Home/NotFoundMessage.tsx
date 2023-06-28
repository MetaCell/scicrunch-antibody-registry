import React from 'react'
import { Box, Container, Stack, Typography, Button } from '@mui/material'
import { AddAntibodyIcon } from '../icons';

const styles = {
  container: {
    height: "100%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  stack: {
    display: "flex",
    justifyContent: "center",
    "& .MuiSvgIcon-fontSizeMedium": {
      fontSize: "3rem",
    },
  },
  message: {
    color: "grey.500",
    maxWidth: "560px",
  },
  button: {
    width: "fit-content",
  },
};

const NotFoundMessage = (props) => {
  
  return (
    <Container maxWidth="xl" sx={styles.container} className='overlay'>
      <Stack direction="column" spacing={3} sx={styles.stack}>
        <Box>
          <img src='../../assets/no-record-found.svg' alt='No record found'/>
        </Box>
        <Typography variant="h1">No record found</Typography>
        <Typography variant="subtitle1" align="center" sx={styles.message}>
        Your search &quot;{props.activeSearch}&quot; did not match any of our records.
        </Typography>
        <Box>
          <Button
            variant="contained"
            color="primary"
            startIcon={
              <AddAntibodyIcon
                sx={{
                  width: "0.9rem",
                }}
              />
            }
            href="/add"
            className='btn-add-antibody'
          >
                      Submit an antibody
          </Button>
        </Box>
      </Stack>
    </Container>
  )
}

export default NotFoundMessage