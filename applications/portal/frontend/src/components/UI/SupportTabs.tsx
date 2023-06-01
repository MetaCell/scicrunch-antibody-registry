import React, { useState } from "react";
import { Link } from "react-router-dom"

import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import { useTheme } from "@mui/material/styles";
import { InfoIconCircle, InfoIconCircleActive, FileQuestionIconActive, FileQuestionIcon, MessageChatSquareIcon, MessageChatSquareIconActive } from "../icons";
import Handshake from '@mui/icons-material/Handshake';
import SubHeader from "./SubHeader";

const SupportTabs = (props) => {
  const theme = useTheme();
  const defaultTabValue = window.location.pathname==='/faq'?0:window.location.pathname==='/contact-us'?1:2;
  const [tabValue, setTabValue] = useState(defaultTabValue)
  const classes = {
    supportBox: {
      width: "100%",
      display: "flex",
      justifyContent: "center",
      borderBottom: `1px solid ${theme.palette.grey[100]}`,
      "& .MuiSvgIcon-root": {
        width: "20px"
      }
    },
    tab: {
      color: theme.palette.grey[500],
    },
  };
  React.useEffect(() => {
    if(window.location.pathname==='/faq'){
      setTabValue(0);
    }
    if(window.location.pathname==='/contact-us'){
      setTabValue(1);
    }
    if(window.location.pathname==='/terms-and-conditions'){
      setTabValue(2);
    }
    if(window.location.pathname==='/membership'){
      setTabValue(3);
    }
  },[tabValue])
  const handleTabChange = (e, newTabValue) => {
    setTabValue(newTabValue);
  }
  return <>
    <SubHeader>Support</SubHeader>
    <Box sx={classes.supportBox}>
      <Tabs value={tabValue} onChange={handleTabChange}>
        <Tab
          value={0}
          sx={classes.tab}
          icon={tabValue === 0 ? <FileQuestionIconActive /> : <FileQuestionIcon />}
          iconPosition="start"
          label="FAQs"
          component={Link}
          to="/faq"
        />
        <Tab
          value={1}
          sx={classes.tab}
          icon={tabValue === 1 ? <MessageChatSquareIconActive /> : <MessageChatSquareIcon />}
          iconPosition="start"
          label="Contact Us"
          component={Link}
          to="/contact-us"
        />
        <Tab
          value={2}
          sx={classes.tab}
          icon={tabValue === 2 ? <InfoIconCircleActive /> : <InfoIconCircle />}
          iconPosition="start"
          label="Terms & Conditions"
          component={Link}
          to="/terms-and-conditions"
        />
        <Tab
          value={3}
          sx={classes.tab}
          icon={ <Handshake fontSize="small" color={tabValue === 3 ? "primary" : "inherit"} />}
          iconPosition="start"
          label="Become a member"
          component={Link}
          to="/membership"
        />
      </Tabs>
    </Box>
    <Box sx={{ my: "3em", }}>
      {props.children}
    </Box>
  </>
}
export default SupportTabs;