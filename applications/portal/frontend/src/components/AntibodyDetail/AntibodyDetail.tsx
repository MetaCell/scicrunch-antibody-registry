import {
  Box,
  Button,
  Container,
  Divider,
  Grid,
  Popover,
  Stack,
  Typography,
  CircularProgress,
  Backdrop,
  Link,
  Alert,
} from "@mui/material";
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { getAntibody } from "../../services/AntibodiesService";
import { useTheme } from "@mui/material/styles";

import SubHeader from "../UI/SubHeader";
import HistoryStepper from "./HistoryStepper";
import { CopyToClipboard } from "react-copy-to-clipboard";
import { CopyIcon, ExternalLinkIcon } from "../icons";
import { Antibody, AntibodyStatusEnum } from "../../rest";
import { getProperCitation } from "../../utils/antibody";

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
  const abId = antibody_id.replace("AB_", "").replace("RRID:", "");
  const [antibodies, setAntibodies] = useState<Antibody[]>(null);
  const [error, setError] = useState<string>(null);
  const accession = document.location.hash ? document.location.hash.split("#")[1]: abId;

  const antibody = antibodies && (antibodies.find(a => a.accession === accession) || antibodies[0]);

  const [anchorCitationPopover, setAnchorCitationPopover] =
    useState<HTMLButtonElement | null>(null);

  const handleClickCitation = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorCitationPopover(event.currentTarget);
  };

  const handleCloseCitation = () => {
    setAnchorCitationPopover(null);
  };

  const open = Boolean(anchorCitationPopover);


  const fetchAntibody = (id) => {
    getAntibody(id)
      .then((res) => {
        if(res.length === 0){
          setError("There is currently no public record with this antibody RRID. This is likely due to this record not yet being curated. Please contact the antibody registry curation team if this antibody is needed for your manuscript. abr-help -at- scicrunch -dot- org")
        }
        return setAntibodies(res);
      },
      () => {
        setError("An unexpected error occurred. Please try again later.")
      })
  };

  
  useEffect(() => fetchAntibody(abId), []);
  if(error) {
    return (
      <Alert sx={{ m: 7 }} severity="error">{error}</Alert>
    )
  }
  if (!antibody) {
    return (
      <Backdrop open={true} sx={{ zIndex: 1000 }}
      >
        <CircularProgress />
      </Backdrop>
    );
  }
  const citation = antibody && getProperCitation(antibody);
  return (
    <>
      <SubHeader>AB_{antibody.abId}</SubHeader>
      <Container id="antibody-detail" maxWidth="lg" sx={{ pb: 2 }}>
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
                  <Typography className="title" variant="h6">Antibody details</Typography>
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
                  <Typography className="ab-name" variant="subtitle2">{antibody.abName}</Typography>
                </Grid>
                <Grid item xs={3}>
                  <Typography variant="h4">ID</Typography>
                  <Typography className="ab-id" variant="subtitle2">
                    AB_{antibody.abId}
                  </Typography>
                </Grid>
                <Grid item xs={3}>
                  <Typography variant="h4">Catalog number</Typography>
                  <Typography className="ab-catnum" variant="subtitle2">
                    {antibody.catalogNum}
                  </Typography>
                </Grid>
                <Grid item xs={3} />
                <Grid item xs={3}>
                  <Typography variant="h4">Target antigen</Typography>
                  <Typography className="ab-target" variant="subtitle2">
                    {antibody.abTarget} - {antibody.targetSpecies.join(", ")}
                  </Typography>
                </Grid>
                
                <Grid item xs={3}>
                  <Typography variant="h4">Clonality</Typography>
                  <Typography className="ab-clonality" variant="subtitle2">
                    {antibody.clonality}
                  </Typography>
                </Grid>
                <Grid item xs={3}>
                  <Typography variant="h4">Clone ID</Typography>
                  <Typography className="ab-cloneid" variant="subtitle2">
                    {antibody.cloneId || "N/A"}
                  </Typography>
                </Grid>
                <Grid item xs={3} />
                <Grid item xs={3}>
                  <Typography variant="h4">Host organism</Typography>
                  <Typography className="ab-sourceorganism" variant="subtitle2">
                    {antibody.sourceOrganism || "N/A"}
                  </Typography>
                </Grid>
              </Grid>
              <Divider />
              <Grid container>
                <Grid item xs={3}>
                  <Typography variant="subtitle1">Proper citation</Typography>
                </Grid>
                <Grid item xs={8}>
                  <Typography className="ab-propercitation" variant="subtitle2">{citation}</Typography>
                  <CopyToClipboard text={citation}>
                    <Button
                      variant="text"
                      size="small"
                      startIcon={
                        <CopyIcon stroke={theme.palette.primary.dark} />
                      }
                      onClick={handleClickCitation}
                      sx={classes.buttonText}
                      className="copy-citation-button"
                    >
                      Copy citation
                    </Button>
                  </CopyToClipboard>
                  <Popover
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
                    className="copy-citation"
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
                  <Typography className="ab-comments" variant="subtitle2" dangerouslySetInnerHTML={{ __html: antibody.comments }} />

                </Grid>
              </Grid>
              <Divider />
              <Grid container>
                <Grid item xs={3}>
                  <Typography variant="subtitle1">Vendor</Typography>
                </Grid>
                <Grid item xs={8}>
                  <Typography className="ab-vendorname" variant="subtitle2">
                    {antibody.vendorName}
                  </Typography>

                  {antibody.url && <Button
                    variant="text"
                    size="small"
                    target="_blank"
                    sx={classes.buttonText}
                    endIcon={
                      <ExternalLinkIcon stroke={theme.palette.primary.dark} />
                    }
                    href={antibody.url}
                    className="open-vendor-website-button"
                  >
                    Open in vendor website
                  </Button>}
                </Grid>
              </Grid>
              <Divider />
              {antibody.status === AntibodyStatusEnum.Curated && (<>
              <Grid container>
                <Grid item xs={3}>
                  <Typography variant="subtitle1">Additional information</Typography>
                </Grid>
                <Grid item xs={8}>
                  {<Button
                    variant="text"
                    target="_blank"
                    size="small"
                    sx={classes.buttonText}
                    endIcon={
                      <ExternalLinkIcon stroke={theme.palette.primary.dark} />
                    }
                    href={`https://scicrunch.org/ResourceWatch/Search?q=AB_${antibody.abId}`}
                    className="open-resourcewatch-button"
                  >
                    See validation in Resource Watch
                  </Button>}
                  {<Button
                    variant="text"
                    target="_blank"
                    size="small"
                    sx={classes.buttonText}
                    endIcon={
                      <ExternalLinkIcon stroke={theme.palette.primary.dark} />
                    }
                    href={`https://scicrunch.org/resolver/RRID:AB_${antibody.abId}`}
                    className="open-resourcewatch-button"
                  >
                    See citations and ratings in Resolver
                  </Button>}
                </Grid>
              </Grid>
              <Divider />
              </>
              )}
              
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
                        className="copy-link-button"
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
        {antibodies && antibodies.length > 1 && 
        <Alert severity="info" className="ab-duplicates-info">Multiple antibodies have been found for this id: showing accession AB_{antibody.accession}. Other entries:&nbsp;
          {antibodies.filter((a) => a.accession != accession).map((a, i, arr) => <>
          <Link href={"#" + a.accession}>
            AB_{a.accession}
          </Link>{i < arr.length - 1 ? ", ": "."}
            </>)}
        </Alert>}
      </Container>
      
    </>
  );
};

export default AntibodyDetail;
