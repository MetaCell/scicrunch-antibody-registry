import React from "react";
import { useHistory } from "react-router-dom";
import { Badge, Box, Button, Stack, Tab, Tabs } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { GridToolbarColumnsButton } from "@mui/x-data-grid";
import { HouseIcon, SendIcon, FilteringIcon } from "../icons";
import { UserContext } from "../../services/UserService";
import { ALLRESULTS } from "../../constants/constants";

const TableToolbar = ({ showFilterMenu, activeTab, filterModel }) => {
  const user = React.useContext(UserContext)[0];
  const theme = useTheme();
  const history = useHistory();
  return (
    <Box
      sx={(theme) => ({
        width: "100%",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        borderBottom: `1px solid ${theme.palette.grey[200]}`,
      })}
    >
      <Tabs
        value={activeTab === ALLRESULTS ? "one" : "two"}
        textColor="primary"
        indicatorColor="primary"
        sx={{
          alignItems: "end",
        }}
      >
        <Tab
          sx={{ p: 0, mr: 1.75, color: "grey.500", minHeight: "56px" }}
          value="one"
          icon={
            <HouseIcon
              stroke={
                activeTab === ALLRESULTS
                  ? theme.palette.primary.main
                  : theme.palette.grey[400]
              }
            />
          }
          iconPosition="start"
          label="All Results"
          onClick={() => history.push("/")}
        />
        <Tab
          sx={{
            p: 0,
            color: "grey.500",
            minHeight: "56px",
            display: !user && "none",
          }}
          value="two"
          icon={
            <SendIcon
              stroke={
                activeTab == "my submissions"
                  ? theme.palette.primary.main
                  : theme.palette.grey[400]
              }
            />
          }
          iconPosition="start"
          label="My Submissions"
          className="btn-submissions"
          onClick={() => history.push("/submissions")}
        />
      </Tabs>
      <Box display="flex" flexDirection="row">
        <Stack direction="row" spacing={3}>
          
          <Button
            variant="text"
            startIcon={<Badge variant="dot" badgeContent={filterModel?.items?.length} color="primary"><FilteringIcon fontSize="small" /></Badge>}
            sx={{
              color: "grey.500",
              fontWeight: 600,
              px: 1.75,
              py: 0.75,
            }}
            onClick={showFilterMenu}
          >
              Filter
          </Button>
          
          
          <GridToolbarColumnsButton size="medium" color="info" />
          
        </Stack>
      </Box>
    </Box>
  );
};

export default TableToolbar;
