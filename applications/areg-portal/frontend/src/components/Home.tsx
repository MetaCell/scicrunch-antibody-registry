import React from "react";
import "../styles/style.less";
import { Container } from "@mui/material";
import AntibodiesTable from "./AntibodiesTable";
import TableHeader from "./TableHeader";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

const Home = () => (
  <Container maxWidth="xl" sx={{ my: 1 }}>
    <TableHeader />
    <AntibodiesTable />
  </Container>
);

export default Home;
