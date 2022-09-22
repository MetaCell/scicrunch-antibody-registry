import * as React from "react";
import { styled } from "@mui/material/styles";
import InputBase from "@mui/material/InputBase";
import { SearchIcon, SlashIcon } from "../icons";
import { Box, Stack } from "@mui/material";

const Search = styled("div")(({ theme }) => ({
  display: "flex",
  flexGrow: 1,
  borderRadius: theme.shape.borderRadius,
  backgroundColor: theme.palette.grey["100"],
  padding: theme.spacing(0.5),
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: theme.palette.grey["600"],
  width: "100%",
  fontSize: "1rem",
  "& .MuiInputBase-input": {
    transition: theme.transitions.create("width"),
    width: "100%",
    [theme.breakpoints.up("md")]: {
      width: "20ch",
    },
  },
}));

export default function Searchbar() {
  return (
    <Search>
      <Stack
        direction="row"
        spacing={1}
        display="flex"
        alignItems="center"
        width="100%"
        sx={{ ml: 1 }}
      >
        <SearchIcon
          sx={{ width: "1.125rem", height: "1.125rem", m: "0.125rem" }}
        />
        <StyledInputBase placeholder="Search for catalog number" />
        <Box
          sx={(theme) => ({
            bgcolor: "grey.200",
            maxHeight: "2rem",
            minWidth: "2rem",
            borderRadius: "0.375rem",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            p: theme.spacing(1),
          })}
        >
          <SlashIcon sx={{ width: "1rem", height: "1rem" }} />
        </Box>
      </Stack>
    </Search>
  );
}
