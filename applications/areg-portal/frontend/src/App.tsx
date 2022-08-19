import React from "react";
import "./styles/style.less";
import { Container, CssBaseline, Stack } from "@mui/material";
import { ThemeProvider } from "@mui/material/styles";

import theme from "./theme/Theme";
import AntibodiesTable from "./components/Home/AntibodiesTable";
import Navbar from "./components/NavBar/Navbar";
import HomeHeader from "./components/Home/HomeHeader";
import TableToolbar from "./components/Home/TableToolbar";

const Main = () => (
  <ThemeProvider theme={theme}>
    <CssBaseline />
    <Navbar />
    <Container maxWidth="xl" sx={{ my: 1 }}>
      <Stack direction="column" spacing={1.5} mb={2}>
        <HomeHeader />
        <TableToolbar />
      </Stack>
      <AntibodiesTable />
    </Container>
  </ThemeProvider>
);

export default Main;
