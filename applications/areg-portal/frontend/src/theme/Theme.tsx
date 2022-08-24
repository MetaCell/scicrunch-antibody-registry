import { createTheme } from "@mui/material/styles";
import { vars } from "./variables";

const { primaryFont, whiteColor, primaryColor, btnBorderColor, shadow } = vars;

declare module "@mui/material/styles" {
  interface Theme {}
  interface ThemeOptions {}
}

const theme = createTheme({
  palette: {
    grey: {
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
    },
    primary: {
      main: "#2173F2",
      light: "#DFEBF8",
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
    subtitle1: {
      fontSize: "0.875rem",
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: `
        * {
          font-family: ${primaryFont}
        }
      `
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
          boxShadow: 'none'
        },

        containedSecondary: {
          background: whiteColor,
          border: `0.0625rem solid ${btnBorderColor}`,
          boxShadow: shadow,
          borderRadius: '0.5rem',
          color: primaryColor,
          fontWeight: 600,
          fontSize: '1rem',
          lineHeight: '1.5rem',

          '&:hover': {
            background: whiteColor,
            boxShadow: shadow,
            color: primaryColor,
          },
        },
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
        },
      },
    },
  },
});

export default theme;
