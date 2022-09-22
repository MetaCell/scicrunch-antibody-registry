import React from "react";
import { Container } from "@mui/material";

import SubHeader from "../UI/SubHeader";
import AccountDetailsForm from "./AccountDetailsForm";

const AccountDetails = () => {
  return (
        <>
            <SubHeader>Good morning, Olivia.</SubHeader>
            <Container maxWidth="lg" disableGutters>
              <AccountDetailsForm/>
            </Container>
        </>
  )

}
export default AccountDetails;