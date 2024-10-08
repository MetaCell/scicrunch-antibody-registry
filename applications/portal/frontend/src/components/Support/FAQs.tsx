import React from "react";

import { vars } from "../../theme/variables";
import { AccordionPlusIcon, AccordionMinusIcon } from "../icons";
import { Box, Typography, Accordion, AccordionSummary, AccordionDetails, Container, Link } from "@mui/material";
import Grid from '@mui/material/Grid2';
import { faqsInfo } from "../../content/faqsInfo";
const { primaryTextColor, primarySubheaderColor, primaryHeaderColor } = vars;
import SupportTabs from "../UI/SupportTabs";


const styles = {
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
};

const FAQ = ({ question, answer, expanded, handleChange }) => {

  return (
    <Accordion defaultExpanded={true} onChange={handleChange} className="faq-container">
      <AccordionSummary
        expandIcon={ expanded ? <AccordionMinusIcon /> : <AccordionPlusIcon />}
        className="faq-summary"
      >
        <Typography component="div" className="faq-question">
          {question}
        </Typography>
      </AccordionSummary>
      <AccordionDetails sx={styles.accordionExpanded} >
        <Typography component="div" className="faq-answer">
          {answer}
        </Typography>
      </AccordionDetails>
    </Accordion>
  )
}

const FAQs = () => {

  const [expanded, setExpanded] = React.useState(faqsInfo.reduce((acc, _, index) => ({ ...acc, [index]: true }), {}));


  return (
    (<SupportTabs>
      <Container maxWidth="lg">
        <Box sx={styles.faqBox}>
          <Typography sx={styles.faqBoxSubheader}>Support</Typography>
          <Typography sx={styles.faqBoxHeader}>FAQs</Typography>
          <Typography sx={styles.faqBoxText}>Everything you need to know about the Antibody Registry. Can’t find the answer you’re looking for? 
            Please contact our team at <Link href="mailto:rii-help@scicrunch.org">rii-help@scicrunch.org</Link></Typography>
        </Box>
      </Container>
      <Grid
        container
        spacing={2}
        direction="row"
        sx={[{
          alignItems: "start",
          justifyContent: "center"
        }, styles.grid]}>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <Box sx={styles.accordion}>
            {
              faqsInfo.slice(0, faqsInfo.length / 2).map(({ question, answer }, index) => <FAQ key={question} question={question} answer={answer} expanded={expanded[index]} handleChange={() => setExpanded({ ...expanded,  [index]: !expanded[index] })} />)
            }
          </Box>
        </Grid>
        <Grid size={{ xs: 12, sm: 6, md: 4 }}>
          <Box sx={styles.accordion}>
            {
              faqsInfo.slice(faqsInfo.length / 2, faqsInfo.length).map(({ question, answer }, index) => <FAQ key={question} question={question} answer={answer} expanded={expanded[index + faqsInfo.length / 2]} handleChange={() => setExpanded({ ...expanded,  [index + faqsInfo.length / 2]: !expanded[index + faqsInfo.length / 2] })} />)
            }
          </Box>
        </Grid>
      </Grid>
    </SupportTabs>)
  );
}
export default FAQs