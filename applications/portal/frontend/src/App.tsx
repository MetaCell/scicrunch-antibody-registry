import React, { useState } from "react";
import { CssBaseline } from "@mui/material";
import { ThemeProvider } from "@mui/material/styles";
import theme from "./theme/Theme";
import Navbar from "./components/NavBar/Navbar";
import About from "./components/About";
import Home from "./components/Home";
import InquirePage from "./components/Support/InquirePage";
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
import UpdateForm from "./components/Update/UpdateForm";
import Footer from "./components/Footer/Footer";
import DownloadPage from "./components/DownloadPage";

function SearchRedirect() {
  const searchParams = new URLSearchParams(window.location.search);
  const query = searchParams.get('q');

  if(query) {
    if(query.startsWith('RRID:') || query.startsWith('AB_')) {
      const id = query?.replace('RRID:', '');
      if (id) {
        const newUrl = `/${id}`;
        return <Redirect to={newUrl} />;
      } else {
        return <Redirect to={"/"} />;
      }
    } else {
      return <>
        <Navbar />
        <Home activeTab={ALLRESULTS} />
      </>
    }
    
  }
  

  return <Redirect to={"/"} />;
}


const App = () => {
  const [user, setUser] = useState(undefined);

  function refreshUser() {
    const u = UserService.getCurrentUserFromCookie();
    if (u && u.sub) {
      UserService.fetchUser(u.sub).then(
        (res: any) => setUser({ ...u, ...res.data }),
        () => setUser(null)
      );
    }

    setUser(u);
    return u;
  }

  if (user === undefined) {
    refreshUser();
    return <></>
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
                <Footer/>
              </Route>
              <Route exact path="/about">
                <Navbar />
                <About />
                <Footer/>
              </Route>
              <Route exact path="/add" component={Submit} />
              <Route path="/login">
                <Redirect to="/" />
              </Route>
              <Route path="/oauth/logout">
                <Redirect to="/" />
              </Route>
              <Route path="/:antibody_id(AB_.*|RRID:AB_.*)">
                <Navbar />
                <AntibodyDetail />
                <Footer/>
              </Route>
              <Route path="/search" render={SearchRedirect} />
              <Route path="/search.php" render={SearchRedirect} />
              <Route path="/user">
                <Navbar />
                <AccountDetails />
                <Footer/>
              </Route>
              <Route path="/faq">
                <Navbar />
                <FAQs />
                <Footer/>
              </Route>
              <Route path="/download">
                <Navbar />
                <DownloadPage />
                <Footer/>
              </Route>
              <Route path="/contact-us">
                <Navbar />
                <ContactUs />
                <Footer/>
              </Route>
              <Route path="/membership">
                <Navbar />
                <InquirePage />
                <Footer/>
              </Route>
              <Route path="/terms-and-conditions">
                <Navbar />
                <TermsAndConditions />
                <Footer/>
              </Route>
              <Route path="/submissions">
                <Navbar />
                <Home activeTab={MYSUBMISSIONS} />
                <Footer/>
              </Route>
              <Route path="/update/:ab_accession_number">
                <Navbar />
                <UpdateForm />
              </Route>
            </Switch>
          </SearchState>
        </UserService.UserContext.Provider>
      </ThemeProvider>
    </BrowserRouter>
  );
};

export default App;
