import React, { useState, useEffect } from "react";
import { useParams, useHistory } from "react-router-dom";
import AntibodyForm from "../UI/AntibodyForm";
import { Antibody } from "../../rest";
import {
  getAntibodyByAccessionNumber,
  updateSubmittedAntibody,
} from "../../services/AntibodiesService";

import * as yup from "yup";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";

const UpdateForm = () => {
  const requiredFieldValidation = yup
    .string()
    .required("The field is mandatory");

  const validationSchema = yup.object().shape({
    //catalogNumber: requiredFieldValidation,
    //vendor: requiredFieldValidation,
    name: requiredFieldValidation,
    host: requiredFieldValidation,
    targetSpecies: requiredFieldValidation,
    antibodyTarget: requiredFieldValidation,
    clonality: requiredFieldValidation,
    url: yup
      .string()
      .url("Please enter a valid URL that starts with http or https")
      .required("This field is mandatory"),
  });

  const { ab_accession_number } = useParams();

  const [antibody, setAntibody] = useState<Antibody>();
  const [initialValues, setInitialValues] = useState({});

  const history = useHistory();

  const fetchAntibody = (accessionNum) => {
    getAntibodyByAccessionNumber(accessionNum)
      .then((res) => {
        setInitialValues(mapInitialValues(res));
        return setAntibody(res);
      })
      .catch((err) => alert(err));
  };

  const updateAntibody = (updatedAntibody) => {
    let ab = { ...updatedAntibody, type: antibody.commercialType };
    updateSubmittedAntibody(ab, ab_accession_number)
      .then(() => {
        history.push("/submissions");
      })
      .catch((error) => alert(error));
  };

  useEffect(() => fetchAntibody(ab_accession_number), []);

  const mapInitialValues = (antibody: Antibody) => ({
    catalogNumber: antibody.catalogNum,
    vendor: antibody.vendorName,
    url: antibody.url,
    name: antibody.abName,
    host: antibody.sourceOrganism,
    targetSpecies: antibody.targetSpecies?.join(","),
    antibodyTarget: antibody.abTarget,
    clonality: antibody.clonality,
    cloneID: antibody.cloneId,
    isotype: antibody.productIsotype,
    conjugate: antibody.productConjugate,
    format: antibody.productForm,
    uniprotID: antibody.uniprotId,
    epitope: antibody.epitope,
    applications: antibody.applications?.join(","),
    citation: antibody.definingCitation,
    comments: antibody.comments,
  });

  return (
    <>
      {antibody ? (
        <AntibodyForm
          initialValues={initialValues}
          validationSchema={validationSchema}
          onSubmit={updateAntibody}
          title="Update Antibody Submission"
          className="update-form"
        />
      ) : (
        <Box
          height="90vh"
          alignItems="center"
          display="flex"
          justifyContent="center"
        >
          <CircularProgress />
        </Box>
      )}
    </>
  );
};

export default UpdateForm;
