import React from "react";
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

const App = () => {
  return (
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Navbar />
        <Switch>
          <Route exact path="/" component={Home} />
          <Route exact path="/about" component={About} />
          <Route path="/submit" component={Submit} />
          <Route path="/login" >
            <Redirect to="/" />
          </Route>
          <Route path="/:antibody_id" component={AntibodyDetail} />
        </Switch>
      </ThemeProvider>
    </BrowserRouter>
  )
};

export default App;
