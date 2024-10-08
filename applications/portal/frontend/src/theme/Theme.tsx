import { ThemeContext } from "@emotion/react";
import { createTheme, darken } from "@mui/material/styles";
import { vars } from "./variables";

const { primaryFont, whiteColor, primaryColor, btnBorderColor, shadow, primaryTextColor } = vars;

declare module "@mui/material/styles" {
  interface Theme {}
  interface ThemeOptions {}
}

const theme = createTheme({
  palette: {
    grey: {
      A100: "#FCFCFD",
      50: "#F9FAFB",
      100: "#F2F4F7",
      200: "#EAECF0",
      300: "#D0D5DD",
      400: "#98A2B3",
      500: "#667085",
      600: "#475467",
      700: "#344054",
      800: "#1D2939",
      900: "#101828",
      A200: "#F9F9FB",
    },
    primary: {
      main: "#2173F2",
      light: "#DFEBF8",
      dark: "#0052CC",
      contrastText: "#A5C8F0",
    },
    error: {
      light: "#D92D20",
      main: "#B42318",
      contrastText: "#FEF3F2",
    },
    success: {
      main: "#027A48",
      contrastText: "#ECFDF3",
    },
    warning: {
      main: "#FDB022",
      contrastText: "#FFFAEB",
    },
  },
  shape: {
    borderRadius: 8,
  },
  mixins: {
    toolbar: {
      "@media(min-width:600px)": { minHeight: 72 },
    },
  },
  typography: {
    fontFamily: primaryFont,
    fontSize: 16,
    h1: {
      fontFamily: primaryFont,
      fontWeight: 600,
      fontSize: "1.875rem",
    },
    h2: {
      fontFamily: "'proxima-nova', 'sans-serif'",
      fontWeight: 600,
      fontSize: "1.125rem",
    },
    h5: {
      fontFamily: "'proxima-nova', 'sans-serif'",
      fontWeight: 500,
      fontSize: "0.875rem",
    },
    h6: {
      fontFamily: "'proxima-nova', 'sans-serif'",
      fontWeight: 600,
      fontSize: "0.875rem",
    },
    body1: {
      fontSize: "0.9rem",
      color: primaryTextColor,
      fontWeight: 400
    },
    subtitle1: {
      fontSize: "0.875rem",
    },
    subtitle2: {
      fontSize: "1rem",
      fontWeight: 600,
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: `
        * {
          font-family: ${primaryFont}
        }
        ::-webkit-scrollbar {
          height: 0.5rem;
          width: 0.5rem;
        }
        body {
          text-align: center;
          background-color: "#eeeeee";
        }
        #root {
          min-height: 100vh;
          display: flex;
          flex-direction: column;
        }
        
        ::-webkit-scrollbar-thumb {
          background-color: ${btnBorderColor};
          border-radius: 3rem;
        }
      `,
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: whiteColor,
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
          boxShadow: "none",
        },
        textInfo: ({ theme }) => ({
          color: theme.palette.grey[500],
          fontWeight: "600",
        }),
        textSecondary: ({ theme }) => ({
          background: theme.palette.primary.light,
          color: theme.palette.primary.dark,
          fontWeight: 600,
          fontSize: "1rem",
          lineHeight: "1.5rem",
          boxShadow: shadow,
          border: `1px solid ${theme.palette.primary.light}`,
          "&:hover": {
            background: theme.palette.primary.light,
            color: theme.palette.common.black,
            boxShadow: shadow,
          },
        }),
        containedSecondary: {
          background: whiteColor,
          border: `0.0625rem solid ${btnBorderColor}`,
          boxShadow: shadow,
          borderRadius: "0.5rem",
          color: primaryColor,
          fontWeight: 600,
          fontSize: "1rem",
          lineHeight: "1.5rem",
          "&:hover": {
            background: whiteColor,
            boxShadow: shadow,
            color: primaryColor,
          },
        },
        contained: ({
          theme
        }) => ({
          borderRadius: "0.375rem",
          fontWeight: 600,
          padding: `${theme.spacing(0.6)} ${theme.spacing(2)}`,
          boxShadow: "0px 1px 2px rgba(16, 24, 40, 0.05)",
          variants: [{
            props: {
              color: "primary"
            },
            style: {
              backgroundColor: theme.palette.primary.main,
              color: theme.palette.common.white,
              boxShadow:
                "0px 1px 2px rgba(16, 24, 40, 0.05),inset 0px -2px 0px rgba(0, 0, 0, 0.25)",
              "&:hover": {
                backgroundColor: darken(theme.palette.primary.main, 0.2),
                boxShadow:
                  "0px 1px 2px rgba(16, 24, 40, 0.05),inset 0px -2px 0px rgba(0, 0, 0, 0.25)",
              },
            }
          }, {
            props: {
              color: "info"
            },
            style: {
              backgroundColor: theme.palette.common.white,
              color: theme.palette.grey[700],
              border: `1px solid ${theme.palette.grey[300]}`,
              "&:hover": {
                backgroundColor: theme.palette.common.white,
              },
              "&.Mui-disabled": {
                color: theme.palette.grey[300],
                borderColor: theme.palette.grey[200],
                backgroundColor: theme.palette.common.white,
                boxShadow: "0px 1px 2px rgba(16, 24, 40, 0.05)",
              },
            }
          }]
        }),
      },
    },
    MuiTab: {
      styleOverrides: {
        root: {
          textTransform: "none",
        },
      },
    },
    MuiLink: {
      styleOverrides: {
        root: {
          borderRadius: "8px !important",
          textDecoration: "none",
        },
      },
    },
    MuiInputBase: {
      styleOverrides: {
        root: {
          fontWeight: 400,
          fontSize: "1rem",
        },
      },
    },
    MuiMenu: {
      styleOverrides: {
        list: {
          padding: 0,
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: ({ theme }) => ({
          padding: theme.spacing(1.5, 2),
        }),
      },
    },
    MuiTooltip: {
      styleOverrides: {
        tooltip: {
          background: "transparent",
          color: "#98A2B3",
          maxWidth: "30rem",
        }
      }
    },
  },
});

export default theme;
