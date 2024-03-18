import React from "react";
import {
  AppBar,
  Box,
  Button,
  Container,
  Divider,
  Stack,
  Toolbar,
  Link,
  Grid,
} from "@mui/material";
import Searchbar from "./Searchbar";
import NavLinks from "./NavLinks";
import HelpMenu from "./HelpMenu";
import { UserContext, User } from "../../services/UserService";
import UserAccountMenu from "./UserAccountMenu";


const Navbar = () => {
  const user: User = React.useContext(UserContext)[0];
  const login = () => {
    window.location.href = "/login";
  };
  return (
    <Box className="container-navbar">
      <AppBar className="top-bar" elevation={0}>
        <Container maxWidth="xl">
          <Toolbar
            sx={{
              display: "flex",
              justifyContent: "space-between",
            }}
            disableGutters
          >
            <Grid container>
              <Grid item md={4}>
                <Box
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    flexGrow: 1,
                    height: "2.5rem",
                  }}
                >
                  <Stack direction="row" spacing={2}>
                    <Link className="logo" href="/">
                      <img src={"/assets/logo.svg"} title="Antibody Registry" alt="Antibody Registry Logo" />
                    </Link>

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
              </Grid>
              <Grid item md={4}>
                <Searchbar />
              </Grid>
              <Grid item md={4}>
                <Box
                  sx={{
                    display: "flex",
                    flexGrow: 1,
                    justifyContent: "flex-end",
                    maxHeight: "2.5rem",
                  }}
                >
                  <Stack direction="row" spacing={1.5}>
                    <HelpMenu />
                    {!user ? (
                      <Button className="btn-login" onClick={login}>Log in / Register</Button>
                    ) : (
                      <UserAccountMenu user={user} />
                    )}
                  </Stack>
                </Box>
              </Grid>
            </Grid>
          </Toolbar>
        </Container>
      </AppBar>
      <Box sx={(theme) => ({ ...theme.mixins.toolbar })} component="div" />
    </Box>
  );
};

export default Navbar;
