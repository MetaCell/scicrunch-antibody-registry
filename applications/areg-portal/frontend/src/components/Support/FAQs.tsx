import React from "react";
import { makeStyles } from '@mui/styles';
import { vars } from "../../theme/variables";
import { AccordionPlusIcon, AccordionMinusIcon } from "../icons";
import { Box, Grid, Typography, Accordion, AccordionSummary, AccordionDetails } from "@mui/material";
import { faqsInfo } from "../../content/faqsInfo";
const { primaryTextColor, primarySubheaderColor, primaryHeaderColor } = vars;
import SupportTabs from "../UI/SupportTabs";
const useStyles = makeStyles(() => ({
  faqBox: {
    textAlign: "left",
  },
  faqBoxSubheader: {
    color: primarySubheaderColor,
    marginBottom: "0.8rem"
  },
  faqBoxHeader: {
    fontSize: "1.125rem",
    color: primaryHeaderColor,
    fontWeight: 600,
    marginBottom: "1.3rem"
  },
  faqBoxText: {
    fontSize: "0.9rem",
    color: primaryTextColor,
    fontWeight: 400
  },
  grid: {
    gap: "4rem",
    "& .MuiGrid-item": {
      paddingTop: 0,
      paddingLeft: 0
    }
  },
  gridAccordion: {
    overflowY: "auto",
  },
  accordion: {
    "& .MuiPaper-root.MuiAccordion-root": {
      backgroundColor: "none",
      padding: "1rem",
      borderRadius: "1rem",
      boxShadow: "none",
      "&:before": {
        backgroundColor: "transparent"
      }
    },
    "& .MuiTypography-root": {
      fontWeight: 500,
      fontSize: "1.1rem",
      color: primaryHeaderColor,
      textAlign: "start"
    },
    "& .MuiPaper-root.MuiAccordion-root.Mui-expanded": {
      backgroundColor: " #F9FAFB",
    }
  },
  accordionExpanded: {
    "& .MuiTypography-root": {
      color: primaryTextColor,
      fontWeight: 400,
      fontSize: "0.875rem"
    }
  }
}))

const FAQs = () => {
  const classes = useStyles();
  const [expanded, setExpanded] = React.useState<string | false>(false);

  const handleChange =
    (panel: string) => (event: React.SyntheticEvent, isExpanded: boolean) => {
      setExpanded(isExpanded ? panel : false);
    };

  return (
    <SupportTabs>
      <Grid container spacing={2} direction="row" alignItems="start" justifyContent="center" className={classes.grid}>
        <Grid item xs={12} sm={6} md={4}>
          <Box className={classes.faqBox}>
            <Typography className={classes.faqBoxSubheader}>Support</Typography>
            <Typography className={classes.faqBoxHeader}>FAQs</Typography>
            <Typography className={classes.faqBoxText}>Everything you need to know about the Antibody Registry. Can’t find the answer you’re looking for? Please chat to our team.</Typography>
          </Box>
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <Box className={classes.accordion}>
            {
              faqsInfo.map(({ question, answer }, index) => {
                return (
                  <Accordion key={index} expanded={expanded === question} onChange={handleChange(question)}>
                    <AccordionSummary
                      expandIcon={expanded === question ? <AccordionMinusIcon /> : <AccordionPlusIcon />}
                    >
                      <Typography>
                        {question}
                      </Typography>
                    </AccordionSummary>
                    <AccordionDetails className={classes.accordionExpanded} >
                      <Typography>
                        {answer}
                      </Typography>
                    </AccordionDetails>
                  </Accordion>
                )
              })
            }
          </Box>
        </Grid>
      </Grid>
    </SupportTabs>
  )
}
export default FAQs