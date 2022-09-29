import React from "react";

import { Container } from "@mui/material";

import AntibodiesTable from "./AntibodiesTable";

const Home = (props) => {
  return (
    <Container maxWidth="xl">
      <AntibodiesTable {...props} />
    </Container>
  );
};

export default Home;
