import React from "react";

import { Box, Container } from "@mui/material";


import AntibodiesTable from "./AntibodiesTable";


import HomeHeader from "./HomeHeader";
import TableToolbar from "./TableToolbar";



const Home = () => {

  return <>
    
      <HomeHeader />
    
    <Container maxWidth="xl">
      <AntibodiesTable />
    </Container>
  </>
}
  

export default Home;