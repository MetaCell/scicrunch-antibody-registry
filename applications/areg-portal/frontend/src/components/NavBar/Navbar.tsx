import React from "react";
import {
  AppBar,
  Box,
  Button,
  Container,
  Divider,
  IconButton,
  Stack,
  Toolbar,
  Link
} from "@mui/material";
import Searchbar from "./Searchbar";
import NavLinks from "./NavLinks";
import { HelpIcon } from "../icons";

const Navbar = () => {
  return (
    <Box>
      <AppBar elevation={0}>
        <Container maxWidth="xl">
          <Toolbar
            sx={{
              display: "flex",
              justifyContent: "space-between",
            }}
            disableGutters
          >
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                flexGrow: 1,
                height: "2.5rem",
              }}
            >
              <Stack direction="row" spacing={2}>
                <Link href="/"><img src="./assets/logo.svg" title="Antibody Registry" /></Link>
                
                <Divider
                  orientation="vertical"
                  flexItem
                  sx={(theme) => ({
                    borderColor: theme.palette.grey[100],
                    borderRightWidth: "1.5px",
                  })}
                />
                <NavLinks />
              </Stack>
            </Box>
            <Searchbar />
            <Box
              sx={{
                display: "flex",
                flexGrow: 1,
                justifyContent: "flex-end",
                maxHeight: "2.5rem",
              }}
            >
              <Stack direction="row" spacing={1.5}>
                <IconButton
                  disableRipple
                  sx={{
                    p: 1.25,
                  }}
                >
                  <HelpIcon
                    sx={{
                      width: "1.25rem",
                      heigth: "1.25rem",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  />
                </IconButton>
                <Button onClick={() => window.location.href = "/login"}>Log in / Register</Button>
              </Stack>
            </Box>
          </Toolbar>
        </Container>
      </AppBar>
      <Box sx={(theme) => ({ ...theme.mixins.toolbar })} component="div" />
    </Box>
  );
};

export default Navbar;
