import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Box, Container } from "@mui/material";
import { makeStyles } from "@mui/styles";
import { vars } from "../../theme/variables";

import SubHeader from "../UI/SubHeader";

export const AntibodyDetail = () => {
  const { antibody_id } = useParams();
  const [antibody, setAntibody] = useState({
    id: "",
  });

  useEffect(
    () =>
      setAntibody({
        id: antibody_id,
      }),
    []
  );

  return <SubHeader>{antibody.id}</SubHeader>;
};

export default AntibodyDetail;
