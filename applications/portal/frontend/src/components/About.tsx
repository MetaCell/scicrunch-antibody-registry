import React from 'react'

import { Box, Button, Container, Divider, Grid, Link, Typography } from '@mui/material';
import Slider from "react-slick";
import { vars } from "../theme/variables";
import { useHistory } from 'react-router-dom';

const { footerBg, whiteColor, sepratorColor, primaryColor, contentBg, contentBorderColor, primaryTextColor, bannerHeadingColor } = vars;

const styles = {
  footer: {
    background: footerBg,
    height: '5rem',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',

    '& .MuiTypography-root': {
      display: 'flex',
      alignItems: 'center',
      fontWeight: 600,
      fontSize: '1rem',
      lineHeight: '1.5rem',
      color: whiteColor,

      '& img': {
        marginLeft: '0.75rem',
        display: 'block',
      },
    },
  },

  mainContent: {
    padding: '5rem 0 11.25rem',
    '& img': {
      display: 'block',
      maxWidth: '100%',
    },

    '& hr': {
      margin: '5rem 0',
      borderColor: sepratorColor,
    },
  },

  contentWithBg: {
    padding: '4.5rem',
    background: contentBg,
    border: `0.0625rem solid ${contentBorderColor}`,
    borderRadius: '1.5rem',
  },

  content: {
    '&:not(:last-child)': {
      marginBottom: '5rem',
    },
    textAlign: 'left',

    '& .MuiGrid-root': {
      '& h3': {
        margin: '2rem 0',
      }
    },

    '& .MuiGrid-grid-md-3': {
      '& h3': {
        margin: '0',
      }
    },

    '& h3': {
      fontWeight: 600,
      fontSize: '1.875rem',
      lineHeight: '2.375rem',
      '& span': {
        fontWeight: 600,
        fontSize: '1.875rem',
        lineHeight: '2.375rem',
        color: primaryColor
      },
    },

    '& p': {
      fontWeight: 400,
      fontSize: '1rem',
      lineHeight: '1.5rem',
      color: primaryTextColor,

      '& a': {
        color: primaryColor,
        cursor: 'pointer',
        '&:not(:hover)': {
          textDecoration: 'none',
        },
      },
    },
  },

  banner: {
    background: contentBorderColor,
    paddingTop: '6.3125rem',
    textAlign: 'center',
    boxShadow: 'inset 0 -7.5rem 7.5rem -5rem rgba(0, 0, 0, 0.1)',
    '& .MuiTypography-root': {
      fontWeight: 600,
      fontSize: '1.875rem',
      lineHeight: '2.375rem',
      color: bannerHeadingColor,

      '& img': {
        margin: '0 auto 1.5rem',
      }
    },

    '& img': {
      display: 'block',
      maxWidth: '100%',
      margin: '7.5rem auto 0',
    },
  },

  bannerWithBg: {
    paddingTop: '9.4375rem',
    backgroundColor: primaryColor,
    boxShadow: 'inset -2.5rem -2.5rem 6.25rem rgba(0, 0, 0, 0.1)',
    backgroundImage: `url('../assets/get-started-bg.svg')`,
    backgroundPosition: 'center top',
    backgroundRepeat: 'no-repeat',

    '& .MuiTypography-root': {
      color: whiteColor,
      marginBottom: '1rem',
    },

    '& img': {
      marginTop: '8.75rem'
    }
  },

  m0: {
    margin: '0 !important',
  }
};

const About = () => {

  const settings = {
    dots: false,
    autoplay: true,
    variableWidth: true,
    arrows: false,
    infinite: true,
    speed: 500,
    slidesToScroll: 1,
    swipeToSlide: true,
    slidesToShow: 3,
    cssEase: "linear"
  };
  const partners = [
    { name: 'thermofisher', url: 'https://www.thermofisher.com/' },
    { name: 'proteintech', url: 'https://www.ptglab.com/' },
    { name: 'biocell', url: 'https://bxcell.com/' },
    { name: 'chromotek', url: 'http://www.chromotek.com/home-of-alpaca-antibodies/' },
    { name: 'jesselllab', url: 'https://jesselllab.com/' },
    { name: 'encorbio', url: 'https://encorbio.com/' },
    { name: 'biolegend', url: 'https://www.biolegend.com/' },
    { name: 'leinco', url: 'https://www.leinco.com/' },
    { name: 'jacksonimmuno', url: 'https://www.jacksonimmuno.com/' },
    { name: 'dshb', url: 'http://dshb.biology.uiowa.edu/' },
    { name: 'immunostar', url: 'http://immunostar.com/' },
    { name: 'neuromab', url: 'http://neuromab.ucdavis.edu/' },
    { name: 'sysy', url: 'https://www.sysy.com/' },
    { name: 'atlasantibodies', url: 'https://atlasantibodies.com/' },
    { name: 'frontier', url: 'https://www.frontier-institute.com/wp/antibodies/?lang=en' },
    { name: 'aeonianbiotech', url: 'https://aeonianbiotech.com/' },
    { name: 'bdbiosciences', url: 'http://www.bdbiosciences.com/us/home' },
    { name: 'miltenyibiotec', url: 'https://www.miltenyibiotec.com/US-en/' },
    { name: 'revmab', url: 'https://www.revmab.com/' },
    { name: 'southernbiotech', url: 'https://www.southernbiotech.com/' },
    { name: 'wagner', url: 'http://gwagner.med.harvard.edu/' },
    { name: 'zebrafish', url: 'https://zebrafish.org/home/guide.php' },
    { name: 'genetex', url: 'https://www.genetex.com/' },
    { name: 'licor', url: 'https://www.licor.com/' },
    { name: 'hytest', url: 'https://www.hytest.fi/home' },
    { name: 'Ansh Labs', url: 'https://www.anshlabs.com/', img: './assets/partners/anshlabs.png' },
    { name: 'Oasis Biofarm', url: 'https://www.oasisbiofarm.net', img: './assets/partners/oasis.png' },
    { name: 'Nittobo Medical', url: 'https://www.nittobo.co.jp/', img: './assets/partners/Nittobo.png' },
    { name: 'SICGEN', url: 'https://sicgen.pt/', img: './assets/partners/Sicgen_antibodies.png' },
    { name: 'Sino Biological', url: 'https://www.sinobiological.com/', img: './assets/partners/Sino-Biological.png' },
    { name: 'Niels Danbolt University of Oslo', url: 'https://www.uio.no/', img: './assets/partners/University_of_Oslo.png' },
    { name: 'NIH', url: 'https://www.nhpreagents.org/', img: './assets/partners/NIH.png' },
    { name: 'ichorbio', url: 'https://ichor.bio/', img: './assets/partners/ichorbio.png' },
    { name: 'Antibodies Incorporated', url: 'https://www.antibodiesinc.com/', img: './assets/partners/antibodies_incorporated.jpg' },
    { name: 'HUABIO', url: 'https://www.huabio.com/', img: './assets/partners/HUABIO.png' },
    { name: 'NanoTag', url: 'https://nano-tag.com/', img: './assets/partners/NanoTag.jpg' },
    { name: 'Institute for Protein Innovation', url: 'https://proteininnovation.org/', img: './assets/partners/Institute_for_Protein_Innovation.png' },
    { name: 'Fujirebio', url: 'https://www.fujirebio.com/en', img: './assets/partners/Fujirebio.jpeg' },
    { name: 'Boster Biological Technology', url: 'https://www.bosterbio.com/', img: './assets/partners/Boster_Biological-logo.png' },
    { name: 'Fujifilm Wako USA', url: 'https://wakousa.com/', img: './assets/partners/fujifilm-wako-chemicals-usa-corporation-logo-vector.png' }
  ]
  const history = useHistory();
  const navigate = () => history.push('/');
  return (
    <>
      <Box sx={styles.banner} className="about-banner">
        <Container maxWidth="xl">
          <Typography>
            <img src='./assets/logo-dark.svg' alt="LOGO" />
            About the Antibody Registry
          </Typography>
          <img src='./assets/ipad.webp' alt="" />
        </Container>
      </Box>
      <Box sx={styles.mainContent} className="about-main">
        <Box sx={styles.content} className="about-content">
          <Typography variant="body1" align='center' marginBottom={1.5} component="h3">
            Antibody Registry Partners
          </Typography>

          <Typography variant="body1" align='center' marginBottom={8}>
            We would like to thank our partners, who submit data to us regularly making author&apos;s jobs easier. Would you like to become a partner? <Link href="/membership">Inquire here</Link>.
          </Typography>

          <Slider {...settings} className="about-slider">
            {
              partners.map((partner, index) => (
                <Box px={3} key={index} className="partner">
                  <a href={partner.url} target="_blank" rel="noreferrer">
                    <Box sx={{
                      display: 'flex !important',
                      alignItems: 'center',
                      justifyContent: 'center',
                      height: '85px',
                      width: '150px',
                    }}>
                      <Box
                        component="img" src={partner.img || `./assets/partners/${partner.name}.svg`}
                        alt={partner.name}
                        title={partner.name}
                        sx={{  filter: "grayscale(1)", width: '100%', '&:hover': { opacity: 0.9 } }} />
                    </Box>
                  </a>
                </Box>
              )
              )
            }
          </Slider>
        </Box>
        <Container maxWidth="xl" className="about-search-info">
          <Divider />
          <Box sx={styles.content}>
            <Grid container spacing={9} alignItems="center">
              <Grid item md={5}>
                <img src='./assets/search-icon.svg' alt="Search icon" />
                <Typography component="h3">
                  <Typography component="span">Search.</Typography> The Antibody Registry gives researchers a way to universally identify antibodies used in their research.
                </Typography>

                <Typography>
                  The Antibody Registry assigns unique and persistent identifiers to each antibody so that they can be referenced within publications. These identifiers only point to a single antibody or kit, this allows the antibody used in your methods section to be identified by humans and search engines.
                </Typography>
              </Grid>
              <Grid item md={7}>
                <img src='./assets/search.svg' alt="Search result skeleton" />
              </Grid>
            </Grid>
          </Box>

          <Box sx={styles.content} className="about-submit-info">
            <Grid container spacing={9} alignItems="center">
              <Grid item md={7}>
                <img src='./assets/submit.svg' alt="Plus icon" />
              </Grid>
              <Grid item md={5}>
                <img src='./assets/submit-icon.svg' alt="SUBMIT" />
                <Typography component="h3">
                  <Typography component="span">Submit.</Typography> If the antibody that you are using does not appear via search, help the community by submitting it to us.
                </Typography>

                <Typography>
                  Our curators will review your submission, find information on the antibody and technical data sheets. Home-grown antibodies may be added as well. After submitting an antibody, a permanent identifier will be assigned. This identifier can be quickly traced back in The Antibody Registry.
                </Typography>
              </Grid>
            </Grid>
          </Box>

          <Box sx={styles.content} className="about-records-info">
            <Grid container spacing={9} alignItems="center">
              <Grid item md={5}>
                <img src='./assets/trace-icon.svg' alt="Trace icon" />
                <Typography component="h3">
                  <Typography component="span">Trace.</Typography> We never delete records, so when an antibody changes, we still can trace its provenance.
                </Typography>

                <Typography>
                  We never delete records, so even when an antibody disappears from a vendor&apos;s catalog, or is sold to another vendor, we can trace the provenance of that antibody. (Bandrowski et al).
                </Typography>
              </Grid>
              <Grid item md={7}>
                <img src='./assets/trace.webp' alt="Trace timeline" />
              </Grid>
            </Grid>
          </Box>

          <Box sx={{ ...styles.content, ...styles.contentWithBg }} className="about-database-info">
            <Grid container spacing={9} alignItems="center">
              <Grid item md={3}>
                <Typography component="h3" sx={styles.m0}>
                  Integration with The Journal of Comparative Neurology
                </Typography>
              </Grid>
              <Grid item md={9}>
                <Typography>
                  The Antibody Registry is proud to announce that as of May 2011 we are working with the antibody database provided by the Journal of Comparative Neurology. This database was created by Dr. Clifford Saper, who implemented visionary policy that requires a rigorous categorization of all antibodies used in manuscripts submitted to the journal. This collaboration allows the antibody registry to add important links between heavily used antibodies and all antibodies available for a particular antigen, especially those useful for research in neuroscience. The simple search of the registry has also been updated to reflect the relative importance of the antibodies used in papers found in the Journal of Comparative Neurology.
                </Typography>
              </Grid>
            </Grid>
          </Box>
        </Container>
      </Box>
      <Box sx={{ ...styles.banner, ...styles.bannerWithBg }} className="about-call">
        <Container maxWidth="xl">
          <Typography>
            Ready to get started?
          </Typography>
          <Button className="go-home-button" variant="contained" color='secondary' onClick={navigate}>Search for antibodies</Button>
          <img src="./assets/ipad.webp" width="100%" alt="" />
        </Container>
      </Box>
      <Box sx={styles.footer} className="about-footer">
        <Typography variant="body1">
          Powered by
          <a href="https://www.metacell.us/" target="_blank" rel="noreferrer">
            <img src='./assets/matacell.svg' alt="metacell" />
          </a>
        </Typography>
      </Box>
    </>
  )
}

export default About;