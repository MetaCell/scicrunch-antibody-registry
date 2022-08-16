import { useMediaQuery } from "@mui/material";
import { createTheme } from "@mui/material/styles";

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
    fontFamily: "'proxima-nova', 'sans-serif'",
    fontSize: 16,
    h1: {
      fontFamily: "'proxima-nova', 'sans-serif'",
      fontWeight: 600,
      fontSize: "1.875rem",
    },
    h6: {
      fontFamily: "'proxima-nova', 'sans-serif'",
      fontWeight: 600,
      fontSize: "0.875rem",
    },
    subtitle1: {
      fontSize: "0.875rem",
    },
  },
  components: {
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: "#fff",
        },
      },
    },

    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
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
          textDecoration: "none",
        },
      },
    },
  },
});

export default theme;
