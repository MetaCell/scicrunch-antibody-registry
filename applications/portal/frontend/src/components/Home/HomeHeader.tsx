import React, { useContext } from "react";
import Pluralize from "pluralize";
import useScrollTrigger from "@mui/material/useScrollTrigger";
import {
  Alert,
  AppBar,
  Box,
  Button,
  Container,
  Grid,
  Stack,
  Typography,
} from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { AddAntibodyIcon, DownloadIcon } from "../icons";
import TableToolbar from "./TableToolbar";
import searchContext from "../../context/search/SearchContext";

interface Props {
  /**
   * Injected by the documentation to work in an iframe.
   * You won't need it on your project.
   */
  window?: () => Window;
  children: React.ReactElement;
}
const HideOnScroll = (props: Props) => {
  const { children } = props;

  const trigger = useScrollTrigger();

  return <Box display={trigger ? "none" : "block"}>{children}</Box>;
};

const HomeHeader = ({ activeSelection, handleExport, showFilterMenu, activeTab, shownResultsNum }) => {
  const theme = useTheme();
 
  const { activeSearch, totalElements, lastUpdate } = useContext(searchContext)

  return (
    <Box className="container-home-header">
      <AppBar elevation={0} sx={{ top: "4.5rem" }}>
        <Container maxWidth="xl">
          <Stack direction="column" spacing={1.5} mb={1} width="100%">
            <HideOnScroll>
              <Box display="flex" mt={6} justifyContent="space-between">
                <Box>
                  <Grid container columnSpacing={1.5} rowSpacing={1}>
                    <Grid item>
                      <Typography variant="h1" color="grey.700" align="left">
                        Antibody Registry <sub>beta</sub>
                      </Typography>
                    </Grid>
                    <Grid item display="flex" alignItems="center">
                      <Box
                        bgcolor="primary.main"
                        borderRadius={2}
                        py={0.25}
                        px={1.25}
                        className="search-info"
                      >
                        <Typography
                          variant="h6"
                          color="common.white"
                          align="left"
                        >
                          <span className="total-elements">{totalElements && totalElements?.toLocaleString('en-US')}</span> {Pluralize("antibody",totalElements)}
                          <span className="active-search">{activeSearch && ` for "${activeSearch}"` }</span>
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={12}>
                      <Typography
                        variant="subtitle1"
                        color="grey.400"
                        align="left"
                        className="last-updated"
                      >
                        Last Updated: {lastUpdate?.toLocaleString('en-US', { day: '2-digit', month:'long', weekday: "long" })}
                      </Typography>
                    </Grid>
                  </Grid>
                </Box>
                <Box>
                  <Stack direction="row" spacing={1.5}>
                    <Button
                      disabled={!activeSelection}
                      variant="contained"
                      color="info"
                      onClick={() => handleExport({})}
                      className="btn-download-selection"
                      startIcon={
                        <DownloadIcon
                          stroke={
                            activeSelection
                              ? theme.palette.grey[700]
                              : theme.palette.grey[300]
                          }
                          fontSize="small"
                        />
                      }
                    >
                      Download selection
                    </Button>
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
                      className="btn-submit-antibody"
                    >
                      Submit an antibody
                    </Button>
                  </Stack>
                </Box>
              </Box>
            </HideOnScroll>
            {shownResultsNum < totalElements && activeSearch && (
              <Alert className="limit-alert" severity="warning" sx={{ mt: 1, mb: 1 }}>The search results are limited to a maximum of {shownResultsNum} elements. 
    Please refine your search if you cannot find the antibody you&apos;re looking for.
              </Alert>)
            }
            <TableToolbar
              showFilterMenu={showFilterMenu}
              activeTab={activeTab}
            />
          </Stack>
        </Container>
      </AppBar>
      <Box sx={{ height: "12.5rem" }} component="div" />
    </Box>
  );
};

export default HomeHeader;
