import React from "react";
import { makeStyles } from '@mui/styles';
import { vars } from "../../theme/variables";
import { AccordionPlusIcon, AccordionMinusIcon } from "../icons";
import { Box, Grid, Typography, Accordion, AccordionSummary, AccordionDetails, Container } from "@mui/material";
import { faqsInfo } from "../../content/faqsInfo";
const { primaryTextColor, primarySubheaderColor, primaryHeaderColor } = vars;
import SupportTabs from "../UI/SupportTabs";


const useStyles = makeStyles(() => ({
  faqBox: {
    textAlign: "left",
    marginBottom: "2em"
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

const FAQ = ({ question, answer, expanded, handleChange }) => {
  const classes = useStyles();
  return (
    <Accordion defaultExpanded={true} onChange={handleChange}>
      <AccordionSummary
        expandIcon={ expanded ? <AccordionMinusIcon /> : <AccordionPlusIcon />}
      >
        <Typography component="div">
          {question}
        </Typography>
      </AccordionSummary>
      <AccordionDetails className={classes.accordionExpanded} >
        <Typography component="div">
          {answer}
        </Typography>
      </AccordionDetails>
    </Accordion>
  )
}

const FAQs = () => {
  const classes = useStyles();
  const [expanded, setExpanded] = React.useState(faqsInfo.reduce((acc, _, index) => ({ ...acc, [index]: true }), {}));


  return (
    <SupportTabs>
      <Container maxWidth="lg">
        <Box className={classes.faqBox}>
          <Typography className={classes.faqBoxSubheader}>Support</Typography>
          <Typography className={classes.faqBoxHeader}>FAQs</Typography>
          <Typography className={classes.faqBoxText}>Everything you need to know about the Antibody Registry. Can’t find the answer you’re looking for? Please chat to our team.</Typography>
        </Box>
      </Container>
      <Grid container spacing={2} direction="row" alignItems="start" justifyContent="center" className={classes.grid}>
        <Grid item xs={12} sm={6} md={4}>
          <Box className={classes.accordion}>
            {
              faqsInfo.slice(0, faqsInfo.length / 2).map(({ question, answer }, index) => <FAQ key={question} question={question} answer={answer} expanded={expanded[index]} handleChange={() => setExpanded({ ...expanded,  [index]: !expanded[index] })} />)
            }
          </Box>
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <Box className={classes.accordion}>
            {
              faqsInfo.slice(faqsInfo.length / 2, faqsInfo.length).map(({ question, answer }, index) => <FAQ key={question} question={question} answer={answer} expanded={expanded[index + faqsInfo.length / 2]} handleChange={() => setExpanded({ ...expanded,  [index + faqsInfo.length / 2]: !expanded[index + faqsInfo.length / 2] })} />)
            }
          </Box>
        </Grid>
      </Grid>
    </SupportTabs>
  )
}
export default FAQs