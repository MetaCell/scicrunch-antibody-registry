import React from "react";
import "./styles/style.less";
import { CssBaseline } from "@mui/material";
import { ThemeProvider } from "@mui/material/styles";
import theme from "./theme/Theme";
import Navbar from "./components/NavBar/Navbar";
import About from "./components/About";
import Home from "./components/Home";
import { BrowserRouter, Route, Switch } from "react-router-dom";

const App = () => {
  return (
    <BrowserRouter>
      <ThemeProvider theme={theme}>
      <CssBaseline />
      <Navbar />
      <Switch>
        <Route exact path="/" component={Home} />
        <Route exact path="/about" component={About} />
      </Switch>
      </ThemeProvider>
    </BrowserRouter>
  )
};

export default App;
