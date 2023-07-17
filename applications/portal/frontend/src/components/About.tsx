import React from 'react'
import { makeStyles } from '@mui/styles';
import { Box, Button, Container, Divider, Grid, Link, Typography } from '@mui/material';
import Slider from "react-slick";
import { vars } from "../theme/variables";
import { useHistory } from 'react-router-dom';
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
const { footerBg, whiteColor, sepratorColor, primaryColor, contentBg, contentBorderColor, primaryTextColor, bannerHeadingColor } = vars;

const useStyles = makeStyles(() => ({
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
}));

const About = () => {
  const classes = useStyles();
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
    { name: 'thermofisher', url: 'https://www.thermofisher.com/', src: '1.svg' },
    { name: 'proteintech', url: 'https://www.ptglab.com/', src: '2.svg'  },
    { name: 'biocell', url: 'https://bxcell.com/', src: '3.svg'  },
    { name: 'chromotek', url: 'http://www.chromotek.com/home-of-alpaca-antibodies/', src: '4.svg'  },
    { name: 'jesselllab', url: 'https://jesselllab.com/', src: '5.svg'  },
    { name: 'encorbio', url: 'https://encorbio.com/', src: '6.svg'  },
    { name: 'biolegend', url: 'https://www.biolegend.com/', src: '7.svg'  },
    { name: 'fortis', url: 'https://www.fortislife.com/', src: '8.svg'  },
    { name: 'leinco', url: 'https://www.leinco.com/', src: '9.svg'  },
    { name: 'jacksonimmuno', url: 'https://www.jacksonimmuno.com/', src: '10.svg' },
    { name: 'dshb', url: 'http://dshb.biology.uiowa.edu/', src: '13.svg' },
    { name: 'immunostar', url: 'http://immunostar.com/', src: '14.svg' },
    { name: 'neuromab', url: 'http://neuromab.ucdavis.edu/', src: '15.svg' },
    { name: 'sysy', url: 'https://www.sysy.com/', src: '16.svg' },
    { name: 'atlasantibodies', url: 'https://atlasantibodies.com/', src: '17.svg' },
    { name: 'frontier', url: 'https://www.frontier-institute.com/wp/antibodies/?lang=en', src: '18.svg' },
    { name: 'aeonianbiotech', url: 'https://aeonianbiotech.com/', src: '19.svg' },
    { name: 'bdbiosciences', url: 'http://www.bdbiosciences.com/us/home', src: '20.svg' },
    { name: 'miltenyibiotec', url: 'https://www.miltenyibiotec.com/US-en/', src: '21.svg' },
    { name: 'revmab', url: 'https://www.revmab.com/', src: '22.svg' },
    { name: 'southernbiotech', url: 'https://www.southernbiotech.com/', src: '23.svg' },
    { name: 'wagner', url: 'http://gwagner.med.harvard.edu/', src: '25.svg' },
    { name: 'zebrafish', url: 'https://zebrafish.org/home/guide.php', src: '26.svg' },
    { name: 'genetex', url: 'https://www.genetex.com/', src: '27.svg' },
    { name: 'licor', url: 'https://www.licor.com/', src: '29.svg' },
    { name: 'hytest', url: 'https://www.hytest.fi/home', src: '30.svg' },
    { name: 'OasisBiofarm', url: 'https://www.cytoskeleton.com/', src: '31.png' },
    { name: 'NittoboMedical', url: 'https://www.cytoskeleton.com/', src: '32.png' },
    { name: 'SICGEN', url: 'https://www.cytoskeleton.com/', src: '33.png' },
    { name: 'SinoBiological', url: 'https://www.cytoskeleton.com/', src: '34.png' },
    { name: 'NielsDanboltUniversityofOslo', url: 'https://www.cytoskeleton.com/', src: '35.png' },
    { name: 'NIH', url: 'https://www.cytoskeleton.com/', src: '36.png' },
    { name: 'ichorbio', url: 'https://www.cytoskeleton.com/', src: '37.png' },
  ]
  const history = useHistory();
  const navigate = () => history.push('/');
  return (
    <>
      <Box className={classes.banner}>
        <Container maxWidth="xl">
          <Typography>
            <img src='./assets/logo-dark.svg' alt="LOGO" />
            About the Antibody Registry
          </Typography>
          <img src='./assets/ipad.webp' alt="" />
        </Container>
      </Box>
      <Box className={classes.mainContent}>
        <Box className={classes.content}>
          <Typography align='center' marginBottom={1.5} component="h3">
            Antibody Registry Partners
          </Typography>

          <Typography align='center' marginBottom={8}>
            We would like to thank our partners, who submit data to us regularly making author's jobs easier. Would you like to become a partner? <Link href="#">Inquire here</Link>.
          </Typography>

          <Slider {...settings}>
            {
              partners.map((elementInArray, index) => (
                <Box px={3} key={index}>
                  <a href={elementInArray.url} target="_blank" rel="noreferrer">
                    <Box sx={{
                      display: 'flex !important',
                      alignItems: 'center',
                      justifyContent: 'center',
                      height: '100px',
                      width: '100px',
                    }}>
                      <img src={`./assets/partners/${elementInArray.src}`} alt={elementInArray.name} width='100%' />
                    </Box>
                  </a>
                </Box>
              )
              )
            }
          </Slider>
        </Box>
        <Container maxWidth="xl">
          <Divider />
          <Box className={classes.content}>
            <Grid container spacing={9} alignItems="center">
              <Grid item md={5}>
                <img src='./assets/search-icon.svg' alt="SEARCH" />
                <Typography component="h3">
                  <Typography component="span">Search.</Typography> The Antibody Registry gives researchers a way to universally identify antibodies used in their research.
                </Typography>

                <Typography>
                  The Antibody Registry assigns unique and persistent identifiers to each antibody so that they can be referenced within publications. These identifiers only point to a single antibody or kit, this allows the antibody used in your methods section to be identified by humans and search engines.
                </Typography>
              </Grid>
              <Grid item md={7}>
                <img src='./assets/search.svg' alt="SEARCH" />
              </Grid>
            </Grid>
          </Box>

          <Box className={classes.content}>
            <Grid container spacing={9} alignItems="center">
              <Grid item md={7}>
                <img src='./assets/submit.svg' alt="SUBMIT" />
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

          <Box className={classes.content}>
            <Grid container spacing={9} alignItems="center">
              <Grid item md={5}>
                <img src='./assets/trace-icon.svg' alt="TRACE" />
                <Typography component="h3">
                  <Typography component="span">Trace.</Typography> We never delete records, so when an antibody changes, we still can trace its provenance.
                </Typography>

                <Typography>
                  We never delete records, so even when an antibody disappears from a vendor's catalog, or is sold to another vendor, we can trace the provenance of that antibody. (Bandrowski et al).
                </Typography>
              </Grid>
              <Grid item md={7}>
                <img src='./assets/trace.webp' alt="TRACE" />
              </Grid>
            </Grid>
          </Box>

          <Box className={`${classes.content} ${classes.contentWithBg}`}>
            <Grid container spacing={9} alignItems="center">
              <Grid item md={3}>
                <Typography component="h3" className={classes.m0}>
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
      <Box className={`${classes.banner} ${classes.bannerWithBg}`}>
        <Container maxWidth="xl">
          <Typography>
            Ready to get started?
          </Typography>
          <Button variant="contained" color='secondary' onClick={navigate}>Search for antibodies</Button>
          <img src="./assets/ipad.webp" width='100%' alt="" />
        </Container>
      </Box>
      <Box className={classes.footer}>
        <Typography>
          Powered by
          <a href="https://www.metacell.us/" target="_blank">
            <img src='./assets/matacell.svg' alt="metacell" />
          </a>
        </Typography>
      </Box>
    </>
  )
}

export default About;