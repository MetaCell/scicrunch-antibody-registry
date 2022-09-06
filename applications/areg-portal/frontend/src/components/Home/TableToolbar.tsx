import React, { useState } from "react";
import { Box, Button, Stack, Tab, Tabs } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { GridToolbarColumnsButton } from "@mui/x-data-grid";
import { HouseIcon, SendIcon, FilteringIcon } from "../icons";

const TableToolbar = ({ showFilterMenu }) => {
  const theme = useTheme();
  const [value, setValue] = useState("one");

  const handleChange = (event: React.SyntheticEvent, newValue: string) => {
    setValue(newValue);
  };

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
        value={value}
        onChange={handleChange}
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
                value == "one"
                  ? theme.palette.primary.main
                  : theme.palette.grey[400]
              }
            />
          }
          iconPosition="start"
          label="All Results"
        />
        <Tab
          sx={{ p: 0, color: "grey.500", minHeight: "56px" }}
          value="two"
          icon={
            <SendIcon
              stroke={
                value == "two"
                  ? theme.palette.primary.main
                  : theme.palette.grey[400]
              }
            />
          }
          iconPosition="start"
          label="My Submissions"
        />
      </Tabs>
      <Box display="flex" flexDirection="row">
        <Stack direction="row" spacing={3}>
          <Button
            variant="text"
            startIcon={<FilteringIcon />}
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
