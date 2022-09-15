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
} from "@mui/material";
import Searchbar from "./Searchbar";
import NavLinks from "./NavLinks";
import HelpMenu from "./HelpMenu";
import { useUser, User } from "../../services/UserService"
import UserAccountMenu from "./UserAccountMenu";

const Navbar = () => {
  const user: User = useUser();
  const [isLoggedIn, setIsLoggedIn] = React.useState<boolean>(false)
  const login = () => {

    window.location.href = "/login";
    setIsLoggedIn(true);
    localStorage.setItem("isUserLogIn","1");
  }
  React.useEffect(() => {
    let userIsLogIn = localStorage.getItem("isUserLogIn");
    if(userIsLogIn==="1"){
      setIsLoggedIn(true);
    }
  }, [])
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
                <Link href="/">
                  <img src="./assets/logo.svg" title="Antibody Registry" />
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
                <HelpMenu />
                {!isLoggedIn ? <Button onClick={login}>
                  Log in / Register
                </Button> : <UserAccountMenu user={user} />}
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
