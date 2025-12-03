import React from "react";
import { Container } from "@mui/material";
import { UserContext, User } from "../../services/UserService"
import SubHeader from "../UI/SubHeader";
import AccountDetailsForm from "./AccountDetailsForm";

const AccountDetails = () => {
  const user: User = React.useContext(UserContext)[0];
  return (
    <>
      <SubHeader>Good morning, {user.preferredUsername}.</SubHeader>
      <Container maxWidth="lg" disableGutters>
        <AccountDetailsForm />
      </Container>
    </>
  )

}
export default AccountDetails;