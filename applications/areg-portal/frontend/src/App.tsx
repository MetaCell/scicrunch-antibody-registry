import React from "react";
import "./styles/style.less";
import { Container, CssBaseline, Stack, Box } from "@mui/material";
import { ThemeProvider } from "@mui/material/styles";

import theme from "./theme/Theme";
import AntibodiesTable from "./components/Home/AntibodiesTable";
import Navbar from "./components/NavBar/Navbar";
import HomeHeader from "./components/Home/HomeHeader";

const Main = () => (
  <ThemeProvider theme={theme}>
    <CssBaseline />
    <Navbar />
    <HomeHeader />
    <Container maxWidth="xl">
      <AntibodiesTable />
    </Container>
  </ThemeProvider>
);

export default Main;
