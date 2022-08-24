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
        marginLeft: '0.75rem'
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
  const partners = 10;
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
          <img src='./assets/ipad.png' alt="" />
        </Container>
      </Box>
      <Box className={classes.mainContent}>
        <Box className={classes.content}>
          <Typography align='center' marginBottom={1.5} component="h3">
            Antibody Registry Partners
          </Typography>

          <Typography align='center' marginBottom={8}>
            We would like to thank our partners, who submit data to us regularly making author's jobs easier. Would you like to become a partner? <Link>Inquire here</Link>.
          </Typography>

          <Slider {...settings}>
            {
              [...Array(partners)].map((elementInArray, index) => (
                  <Box px={3} key={index}>
                    <img src={`./assets/partners/${index+1}.svg`} alt="" />
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
                <img src='./assets/trace.svg' alt="TRACE" />
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
          <img src="./assets/ipad.png" alt="" />
        </Container>
      </Box>
      <Box className={classes.footer}>
        <Typography>
          Powered by
          <img src='./assets/matacell.svg' alt="metacell" />
        </Typography>
      </Box>
    </>
  )
}

export default About;