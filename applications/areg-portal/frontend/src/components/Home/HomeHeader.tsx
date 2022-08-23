import React from "react";
import { AppBar, Box, Container, Grid, Stack, Typography } from "@mui/material";
import StyledButton from "../StyledButton";
import { AddAntibodyIcon, DownloadIcon } from "../icons";
import TableToolbar from "./TableToolbar";

const HomeHeader = () => {
  return (
    <Box>
      <AppBar elevation={0} sx={{ top: "4.5rem" }}>
        <Container maxWidth="xl">
          <Stack direction="column" spacing={1.5} mb={2}>
            <Box
              display="flex"
              height="4.125rem"
              mt={6}
              justifyContent="space-between"
            >
              <Box width="23.75rem">
                <Grid container columnSpacing={1.5} rowSpacing={1}>
                  <Grid item>
                    <Typography variant="h1" color="grey.700" align="left">
                      Antibody Registry
                    </Typography>
                  </Grid>
                  <Grid item display="flex" alignItems="center">
                    <Box
                      bgcolor="primary.main"
                      borderRadius={2}
                      py={0.25}
                      px={1.25}
                    >
                      <Typography
                        variant="h6"
                        color="common.white"
                        align="left"
                      >
                        2,512,817 records
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography
                      variant="subtitle1"
                      color="grey.400"
                      align="left"
                    >
                      Last Updated: Friday, 15th July
                    </Typography>
                  </Grid>
                </Grid>
              </Box>
              <Box>
                <Stack direction="row" spacing={1.5}>
                  <StyledButton disabled>
                    <Box
                      sx={{
                        minWidth: "1.25rem",
                        maxHeight: "1.25rem",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        mr: 1,
                      }}
                    >
                      <DownloadIcon
                        sx={{
                          width: "1.25rem",
                        }}
                      />
                    </Box>
                    Download selection
                  </StyledButton>
                  <StyledButton bgPrimary>
                    <Box
                      sx={{
                        minWidth: "1.25rem",
                        maxHeight: "1.25rem",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        mr: 1,
                      }}
                    >
                      <AddAntibodyIcon
                        sx={{
                          width: "0.9rem",
                        }}
                      />
                    </Box>
                    Submit an antibody
                  </StyledButton>
                </Stack>
              </Box>
            </Box>
            <TableToolbar />
          </Stack>
        </Container>
      </AppBar>
      <Box sx={{ height: "12.5rem" }} component="div" />
    </Box>
  );
};

export default HomeHeader;
