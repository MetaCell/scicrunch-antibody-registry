import {
  Box,
  Button,
  Container,
  Divider,
  Grid,
  Stack,
  Typography,
} from "@mui/material";
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { getAntibody } from "../../services/AntibodiesService";
import { useTheme } from "@mui/material/styles";

import SubHeader from "../UI/SubHeader";

export const AntibodyDetail = () => {
  const theme = useTheme();
  const classes = {
    card: {
      padding: theme.spacing(3, 2),
      textAlign: "left",
      "& .MuiTypography-subtitle1": {
        fontSize: "1rem",
        fontWeight: 500,
        color: theme.palette.grey[500],
      },
      "& .MuiTypography-subtitle2": {
        fontSize: "0.875rem",
        fontWeight: 500,
        color: theme.palette.grey[700],
      },
      "& .MuiTypography-h4": {
        fontSize: "0.875rem",
        fontWeight: 400,
        color: theme.palette.grey[500],
      },
    },
    header: {
      "& .MuiTypography-h6": {
        fontSize: "1.125rem",
        color: theme.palette.grey[900],
      },
      "& .MuiTypography-caption": {
        color: theme.palette.grey[500],
      },
    },
  };
  const { antibody_id } = useParams();
  const [antibody, setAntibody] = useState({
    id: "",
    ab_name: "",
    ab_id: "",
    ab_target: "",
    target_species: "",
    proper_citation: "",
    clonality: "",
    comments: "",
    clone_id: "",
    host: "",
    vendor: "",
    catalog_num: 0,
  });

  const fetchAntibody = (id) => {
    getAntibody(id)
      .then((res) => {
        return setAntibody(res);
      })
      .catch((err) => alert(err));
  };

  useEffect(() => fetchAntibody(antibody_id), []);

  return (
    <>
      <SubHeader>{antibody.ab_name}</SubHeader>
      <Container maxWidth="lg">
        <Grid container>
          <Grid item xs={9}>
            <Stack spacing={3} sx={classes.card}>
              <Box
                display="flex"
                flexDirection="row"
                justifyContent="space-between"
                alignItems="flex-start"
                sx={classes.header}
              >
                <Box
                  display="flex"
                  flexDirection="column"
                  alignItems="flex-start"
                >
                  <Typography variant="h6">Antibody details</Typography>
                  <Typography variant="caption">
                    Find all info about this record
                  </Typography>
                </Box>
                <Button variant="contained" color="info" size="small">
                  Submit an edit
                </Button>
              </Box>
              <Divider />
              <Grid container rowSpacing={1}>
                <Grid item xs={3}>
                  <Typography variant="subtitle1">Main Info</Typography>
                </Grid>
                <Grid item xs={3}>
                  <Typography variant="h4">Name</Typography>
                  <Typography variant="subtitle2">{antibody.ab_id}</Typography>
                </Grid>
                <Grid item xs={3}>
                  <Typography variant="h4">ID</Typography>
                  <Typography variant="subtitle2">{antibody.ab_id}</Typography>
                </Grid>
                <Grid item xs={3}>
                  <Typography variant="h4">Target antigen</Typography>
                  <Typography variant="subtitle2">
                    {antibody.ab_target} {antibody.target_species}
                  </Typography>
                </Grid>
                <Grid item xs={3}></Grid>
                <Grid item xs={3}>
                  <Typography variant="h4">Clonality</Typography>
                  <Typography variant="subtitle2">
                    {antibody.clonality}
                  </Typography>
                </Grid>
                <Grid item xs={3}>
                  <Typography variant="h4">Clone ID</Typography>
                  <Typography variant="subtitle2">
                    {antibody.clone_id}
                  </Typography>
                </Grid>
                <Grid item xs={3}>
                  <Typography variant="h4">Host organism</Typography>
                  <Typography variant="subtitle2">{antibody.host}</Typography>
                </Grid>
              </Grid>
              <Divider />
              <Grid container>
                <Grid item xs={3}>
                  <Typography variant="subtitle1">Proper citation</Typography>
                </Grid>
                <Grid item xs={8}>
                  <Typography variant="subtitle2">
                    {antibody.proper_citation}
                  </Typography>
                  <Button variant="text" size="small">
                    Copy citation
                  </Button>
                </Grid>
              </Grid>
              <Divider />
              <Grid container>
                <Grid item xs={3}>
                  <Typography variant="subtitle1">Comments</Typography>
                </Grid>
                <Grid item xs={8}>
                  <Typography variant="subtitle2">
                    {antibody.comments}
                  </Typography>
                </Grid>
              </Grid>
              <Divider />
              <Grid container>
                <Grid item xs={3}>
                  <Typography variant="subtitle1">Vendor</Typography>
                </Grid>
                <Grid item xs={8}>
                  <Typography variant="subtitle2">{antibody.vendor}</Typography>
                  <Button variant="text" size="small">
                    Open in vendor website
                  </Button>
                </Grid>
              </Grid>
              <Divider />
              <Grid container>
                <Grid item xs={3}>
                  <Typography variant="subtitle1">Share</Typography>
                </Grid>
                <Grid item xs={8}>
                  <Typography variant="subtitle2">
                    {window.location.href}
                  </Typography>
                  <Button variant="text" size="small">
                    Copylink
                  </Button>
                </Grid>
              </Grid>
            </Stack>
          </Grid>
          <Grid item xs={3} sx={classes.card}>
            <Box
              display="flex"
              flexDirection="column"
              alignItems="flex-start"
              sx={classes.header}
            >
              <Typography variant="h6">Record History</Typography>
              <Typography variant="caption">
                All history information about this record
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Container>
    </>
  );
};

export default AntibodyDetail;
