import React, { useContext } from "react";
import Pluralize from "pluralize";
import useScrollTrigger from "@mui/material/useScrollTrigger";
import {
  Alert,
  AppBar,
  Box,
  Button,
  Container,
  Stack,
  Typography,
} from "@mui/material";
import Grid from "@mui/material/Grid2";
import { useTheme } from "@mui/material/styles";
import { AddAntibodyIcon, DownloadIcon } from "../icons";
import TableToolbar from "./TableToolbar";
import searchContext from "../../context/search/SearchContext";
import { GridFilterModel } from "@mui/x-data-grid";

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

  return (
    <Box sx={{
      display: trigger ? "none" : "block"
    }}>{children}</Box>
  );
};

type TableHeaderProps = {
  activeSelection: boolean;
  handleExport: (data: any) => void;
  showFilterMenu: () => void;
  activeTab: string;
  shownResultsNum: number;
  warningMessage?: string;
  filterModel: GridFilterModel
};

const TableHeader = (props: TableHeaderProps) => {
  const { activeSelection, handleExport, showFilterMenu, activeTab, warningMessage, filterModel } = props;
  const theme = useTheme();
 
  const { activeSearch, totalElements, lastUpdate, error } = useContext(searchContext)
  const showAlert = warningMessage.length > 0;
  return (
    (<Box className="container-home-header">
      <AppBar elevation={0} sx={{ top: "4.5rem" }}>
        <Container maxWidth="xl">
          <Stack
            direction="column"
            spacing={1.5}
            sx={{
              mb: 1,
              width: "100%"
            }}>
            <HideOnScroll>
              <Box
                sx={{
                  display: "flex",
                  mt: 6,
                  justifyContent: "space-between"
                }}>
                <Box>
                  <Grid container columnSpacing={1.5} rowSpacing={1}>
                    <Grid>
                      <Typography variant="h1" align="left" sx={{
                        color: "grey.700"
                      }}>
                        Antibody Registry <sub>beta</sub>
                      </Typography>
                    </Grid>
                    <Grid
                      sx={{
                        display: "flex",
                        alignItems: "center"
                      }}>
                      <Box
                        className="search-info"
                        sx={{
                          bgcolor: "primary.main",
                          borderRadius: 2,
                          py: 0.25,
                          px: 1.25
                        }}>
                        <Typography
                          variant="h6"
                          align="left"
                          sx={{
                            color: "common.white"
                          }}
                        >
                          <span className="total-elements">{totalElements && totalElements?.toLocaleString('en-US')}</span> {Pluralize("antibody",totalElements)}
                          <span className="active-search">{activeSearch && ` for "${activeSearch}"` }</span>
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid size={12}>
                      <Typography
                        variant="subtitle1"
                        align="left"
                        className="last-updated"
                        sx={{
                          color: "grey.400"
                        }}
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
            {warningMessage && (
              <Alert className="limit-alert" severity="warning" sx={{ mt: 1, mb: 1 }}>
                {warningMessage}
              </Alert>)
            }
            {error && (
              <Alert className="error-alert" severity="error" sx={{ mt: 1, mb: 1 }}>
                {
                  error >= 500 ? 
                    "An error occurred while fetching data. Please try again later. If the problem persists, please contact us at <pre>abr-help -at- scicrunch -dot- org</pre>."
                    : error == 401 ? "This request is unauthorized. Please log in to access this data." : 
                      "Bad request: please try fix your search and filter parameters. If the problem persists, please contact us at <pre>abr-help -at- scicrunch -dot- org</pre>."
                }

              </Alert>)
            }
            <TableToolbar
              showFilterMenu={showFilterMenu}
              activeTab={activeTab}
              filterModel={filterModel}
            />
            
          </Stack>
        </Container>
      </AppBar>
      <Box sx={[showAlert ? {
        height: "16.5rem"
      } : {
        height: "12.5rem"
      }]} component="div" />
    </Box>)
  );
};
export default TableHeader;