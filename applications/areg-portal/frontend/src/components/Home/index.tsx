import React from "react";

import { Container } from "@mui/material";

import AntibodiesTable from "./AntibodiesTable";

const Home = () => {
  return (
    <Container maxWidth="xl">
      <AntibodiesTable />
    </Container>
  );
};

export default Home;
