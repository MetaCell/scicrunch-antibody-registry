import React from "react";
import { Container } from "@mui/material";
import { useUser, User } from "../../services/UserService"
import SubHeader from "../UI/SubHeader";
import AccountDetailsForm from "./AccountDetailsForm";

const AccountDetails = () => {
  const user: User = useUser();
  return (
        <>
            <SubHeader>Good morning, Olivia.</SubHeader>
            <Container maxWidth="lg" disableGutters>
              <AccountDetailsForm user={user}/>
            </Container>
        </>
  )

}
export default AccountDetails;