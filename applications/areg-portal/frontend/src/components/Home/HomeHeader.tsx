import React from "react";
import { Box, Grid, Stack, Typography } from "@mui/material";
import StyledButton from "../StyledButton";
import { AddAntibodyIcon, DownloadIcon } from "../icons";

const HomeHeader = () => {
  return (
    <Box
      height="4.125rem"
      mb={2}
      mt={5}
      display="flex"
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
            <Box bgcolor="primary.main" borderRadius={2} py={0.25} px={1.25}>
              <Typography variant="h6" color="common.white" align="left">
                2,512,817 records
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="subtitle1" color="grey.400" align="left">
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
  );
};

export default HomeHeader;
