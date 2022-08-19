import React from "react";
import { Box, Button, Stack, Tab, Tabs } from "@mui/material";
import { HouseIcon, SendIcon, FilteringIcon, SettingsIcon } from "../icons";

const TableToolbar = () => {
  const [value, setValue] = React.useState("one");

  const handleChange = (event: React.SyntheticEvent, newValue: string) => {
    setValue(newValue);
  };

  return (
    <Box
      sx={{
        width: "100%",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
      <Tabs
        value={value}
        onChange={handleChange}
        textColor="primary"
        indicatorColor="primary"
        sx={{ height: "3.5rem", alignItems: "end" }}
      >
        <Tab
          sx={{ p: 0, mr: 1.75 }}
          value="one"
          icon={<HouseIcon />}
          iconPosition="start"
          label="All Results"
        />
        <Tab
          sx={{ px: 0 }}
          value="two"
          icon={<SendIcon />}
          iconPosition="start"
          label="My Submissions"
        />
      </Tabs>
      <Stack direction="row" spacing={3}>
        <Button
          variant="text"
          startIcon={<FilteringIcon />}
          sx={{ color: "grey.500", fontWeight: 600, px: 1.75, py: 0.75 }}
        >
          Filter
        </Button>
        <Button
          variant="text"
          startIcon={<SettingsIcon />}
          sx={{ color: "grey.500", fontWeight: 600, px: 1.75, py: 0.75 }}
        >
          Table settings
        </Button>
      </Stack>
    </Box>
  );
};

export default TableToolbar;
