import React, { useEffect, useState } from "react";
import { Box, Button, Stack, Tab, Tabs } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import {
  HouseIcon,
  SendIcon,
  FilteringIcon,
  SettingsIcon,
  AddAntibodyIcon,
  DownloadIcon,
} from "../icons";
import StyledButton from "../StyledButton";

const TableToolbar = () => {
  const theme = useTheme();
  const [value, setValue] = useState("one");
  const [scrolling, setScrolling] = useState(false);

  useEffect(() => {
    if (typeof window !== "undefined") {
      window.addEventListener("scroll", () =>
        setScrolling(window.scrollY > 100)
      );
    }
  }, []);

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
        <Stack
          direction="row"
          spacing={1.5}
          ml={1.5}
          display={!scrolling ? "none" : "inherit"}
        >
          <StyledButton disabled>
            <Box
              sx={{
                minWidth: "1.25rem",
                maxHeight: "1.25rem",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                mr: 1,
              }}
            >
              <DownloadIcon
                sx={{
                  width: "1.25rem",
                }}
              />
            </Box>
            Download selection
          </StyledButton>
          <StyledButton bgPrimary>
            <Box
              sx={{
                minWidth: "1.25rem",
                maxHeight: "1.25rem",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                mr: 1,
              }}
            >
              <AddAntibodyIcon
                sx={{
                  width: "0.9rem",
                }}
              />
            </Box>
            Submit an antibody
          </StyledButton>
        </Stack>
      </Box>
    </Box>
  );
};

export default TableToolbar;
