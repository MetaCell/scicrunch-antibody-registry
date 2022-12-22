import React, { useState } from "react";
import "./styles/style.less";
import { CssBaseline } from "@mui/material";
import { ThemeProvider } from "@mui/material/styles";
import theme from "./theme/Theme";
import Navbar from "./components/NavBar/Navbar";
import About from "./components/About";
import Home from "./components/Home";
import AntibodyDetail from "./components/AntibodyDetail";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";
import Submit from "./components/Submit";
import FAQs from "./components/Support/FAQs";
import ContactUs from "./components/Support/ContactUs";
import TermsAndConditions from "./components/Support/TermsAndConditions";
import AccountDetails from "./components/AccountDetails";
import { ALLRESULTS, MYSUBMISSIONS } from "./constants/constants";
import SearchState from "./context/search/SearchState";
import * as UserService from "./services/UserService";

const App = () => {

  const [user, setUser] = useState(undefined);

  function refreshUser() {
    const u = UserService.getCurrentUserFromCookie();
    UserService.fetchUser(u.sub).then((res: any) => setUser({ ...u, ...res.data }), () => setUser(null));
    setUser(u);
    return u;
  }

  if (user === undefined) {
    return [refreshUser(), refreshUser];
  }
 
  return (
    
    <BrowserRouter>
    
      <ThemeProvider theme={theme}>
        <UserService.UserContext.Provider value={[user, refreshUser]}>
          <CssBaseline />
          <SearchState>
          
            <Switch>
              <Route exact path="/">
                <Navbar />
                <Home activeTab={ALLRESULTS} />
              </Route>
              <Route exact path="/about" >
                <Navbar />
                <About />
              </Route>
              <Route exact path="/add" component={Submit} />
              <Route path="/login">
                <Redirect to="/" />
              </Route>
              <Route path="/oauth/logout">
                <Redirect to="/" />
              </Route>
              <Route path="/:antibody_id(AB_.*)">
                <Navbar />
                <AntibodyDetail />
              </Route>
              <Route path="/user" >
                <Navbar />
                <AccountDetails />
              </Route>
              <Route path="/faq">
                <Navbar />
                <FAQs />
              </Route>
              <Route path="/contact-us">
                <Navbar />
                <ContactUs />
              </Route>
              <Route path="/terms-and-conditions" >
                <Navbar />
                <TermsAndConditions />
              </Route>
              <Route path="/submissions">
                <Navbar />
                <Home activeTab={MYSUBMISSIONS} />
              </Route>
            </Switch>
          </SearchState>
        </UserService.UserContext.Provider>
      </ThemeProvider>
    </BrowserRouter>
    
  );
};

export default App;
