import {
  Box,
  Button,
  Container,
  Divider,
  Grid,
  Popover,
  Stack,
  Typography,
} from "@mui/material";
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { getAntibody } from "../../services/AntibodiesService";
import { useTheme } from "@mui/material/styles";

import SubHeader from "../UI/SubHeader";
import HistoryStepper from "./HistoryStepper";
import { CopyToClipboard } from "react-copy-to-clipboard";
import { CopyIcon, ExternalLinkIcon } from "../icons";

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
    buttonText: {
      color: theme.palette.primary.dark,
    },
    buttonGrey: {
      color: theme.palette.grey[700],
      padding: theme.spacing(1, 2),
    },
    inputBox: {
      backgroundColor: theme.palette.grey[50],
    },
    input: {
      flexGrow: 2,
      display: "flex",
      alignItems: "center",
      padding: theme.spacing(0, 1),
      backgroundColor: theme.palette.grey[50],
      borderRight: "solid 1px",
      borderColor: theme.palette.grey[300],
      borderLeft: "solid 1px white",
      borderTopLeftRadius: "8px",
      borderBottomLeftRadius: "8px",
      "& .MuiTypography-root": {
        fontSize: "1rem",
        fontWeight: 400,
        color: theme.palette.grey[500],
      },
    },
    group: {
      border: "solid 1px",
      borderColor: theme.palette.grey[300],
      borderRadius: theme.shape,
    },
    popover: {
      p: 1,
      backgroundColor: theme.palette.grey[900],
      color: theme.palette.common.white,
      fontSize: "1rem",
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
    url: "",
    insert_time: "",
    curate_time: "",
    disc_date: "",
  });

  const [anchorCitationPopover, setAnchorCitationPopover] =
    useState<HTMLButtonElement | null>(null);

  const handleClickCitation = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorCitationPopover(event.currentTarget);
  };

  const handleCloseCitation = () => {
    setAnchorCitationPopover(null);
  };

  const open = Boolean(anchorCitationPopover);
  const id = open ? "simple-popover" : undefined;

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
          <Grid item xs={8}>
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
                  <CopyToClipboard text={antibody.proper_citation}>
                    <Button
                      variant="text"
                      size="small"
                      startIcon={
                        <CopyIcon stroke={theme.palette.primary.dark} />
                      }
                      onClick={handleClickCitation}
                      sx={classes.buttonText}
                    >
                      Copy citation
                    </Button>
                  </CopyToClipboard>
                  <Popover
                    id={id}
                    open={open}
                    anchorEl={anchorCitationPopover}
                    onClose={handleCloseCitation}
                    anchorOrigin={{
                      vertical: "top",
                      horizontal: "right",
                    }}
                    transformOrigin={{
                      vertical: "center",
                      horizontal: "center",
                    }}
                  >
                    <Typography sx={classes.popover}>
                      Citation copied to clipboard
                    </Typography>
                  </Popover>
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

                  <Button
                    variant="text"
                    size="small"
                    sx={classes.buttonText}
                    endIcon={
                      <ExternalLinkIcon stroke={theme.palette.primary.dark} />
                    }
                    href={`https://${antibody.url}`}
                  >
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
                  <Box display="flex" sx={classes.group}>
                    <Box sx={classes.input}>
                      <Typography>{window.location.href}</Typography>
                    </Box>
                    <CopyToClipboard text={window.location.href}>
                      <Button
                        variant="text"
                        color="info"
                        size="small"
                        startIcon={
                          <CopyIcon stroke={theme.palette.grey[700]} />
                        }
                        sx={classes.buttonGrey}
                      >
                        Copy link
                      </Button>
                    </CopyToClipboard>
                  </Box>
                </Grid>
              </Grid>
            </Stack>
          </Grid>
          <Grid item xs={4} sx={classes.card}>
            <HistoryStepper classes={classes} antibody={antibody} />
          </Grid>
        </Grid>
      </Container>
    </>
  );
};

export default AntibodyDetail;
