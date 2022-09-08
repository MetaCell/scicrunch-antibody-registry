import React, { useState } from "react";

import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import { useTheme } from "@mui/material/styles";
import { InfoIconCircle, InfoIconCircleActive, FileQuestionIconActive, FileQuestionIcon, MessageChatSquareIcon, MessageChatSquareIconActive } from "../icons";

import FAQs from "./FAQs";

import SubHeader from "../UI/SubHeader";
import { Container } from "@mui/material";

const Support = () => {
    const theme = useTheme();
    const [tabValue, setTabValue] = useState(0)
    const classes = {
        supportBox: {
            width: "100%",
            display: "flex",
            justifyContent: "center",
            borderBottom: `1px solid ${theme.palette.grey[100]}`,
            "& .MuiSvgIcon-root":{
                width:"20px"
            }
        },
        tab: {
            color: theme.palette.grey[500],
        },
    };
    const handleTabChange = (e, newTabValue) => {
        setTabValue(newTabValue);
    }
    return <>
        <SubHeader>Support</SubHeader>
        <Box sx={classes.supportBox}>
            <Tabs value={tabValue} onChange={handleTabChange}>
                <Tab value={0} sx={classes.tab} icon={tabValue === 0 ? <FileQuestionIconActive /> : <FileQuestionIcon />} iconPosition="start" label="FAQs" />
                <Tab value={1} sx={classes.tab} icon={tabValue === 1 ? <MessageChatSquareIconActive /> : <MessageChatSquareIcon />} iconPosition="start" label="Contact Us" />
                <Tab value={2} sx={classes.tab} icon={tabValue === 2 ? <InfoIconCircleActive /> : <InfoIconCircle />} iconPosition="start" label="Terms & Conditions" />
            </Tabs>
        </Box>
        <Box sx={{marginTop:"95px"}}>
        {
            tabValue === 0 ? <FAQs/>: tabValue === 1 ? <div>Contact us</div> : <div>Terms and conditions</div>
        }
        </Box>
    </>
}
export default Support;