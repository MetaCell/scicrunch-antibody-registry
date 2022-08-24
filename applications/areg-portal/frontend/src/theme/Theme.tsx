import { createTheme } from "@mui/material/styles";
import { darken } from "@mui/material/styles";

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
    subtitle2: {
      fontSize: "1rem",
      fontWeight: 600,
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
        contained: ({ ownerState, theme }) => ({
          borderRadius: "0.375rem",
          fontWeight: 600,
          padding: `${theme.spacing(0.6)} ${theme.spacing(2)}`,
          boxShadow: "0px 1px 2px rgba(16, 24, 40, 0.05)",
          ...(ownerState.color === "primary" && {
            backgroundColor: theme.palette.primary.main,
            color: theme.palette.common.white,
            boxShadow:
              "0px 1px 2px rgba(16, 24, 40, 0.05),inset 0px -2px 0px rgba(0, 0, 0, 0.25)",
            "&:hover": {
              backgroundColor: darken(theme.palette.primary.main, 0.2),
              boxShadow:
                "0px 1px 2px rgba(16, 24, 40, 0.05),inset 0px -2px 0px rgba(0, 0, 0, 0.25)",
            },
          }),
          ...(ownerState.color === "secondary" && {
            backgroundColor: theme.palette.common.white,
            color: theme.palette.grey[700],
            border: `1px solid ${theme.palette.grey[300]}`,
            "&.Mui-disabled": {
              color: theme.palette.grey[300],
              borderColor: theme.palette.grey[200],
              backgroundColor: theme.palette.common.white,
              boxShadow: "0px 1px 2px rgba(16, 24, 40, 0.05)",
            },
          }),
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
  },
});

export default theme;
