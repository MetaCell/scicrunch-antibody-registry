import React from "react";
import {
  IconButton,
  Menu,
  MenuList,
  MenuItem,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography,
  Divider,
  Stack,
  Box,
} from "@mui/material";
import {
  GridToolbarColumnsButton,
  GridColumnsMenuItem,
} from "@mui/x-data-grid";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import { SortByIcon, ViewLayoutIcon } from "../icons";

const TableSettingsMenu = (props) => {
  const { anchorEl, setAnchorEl, open } = props;

  const handleClose = () => {
    setAnchorEl(null);
  };
  return (
    <Menu
      id="settings-menu"
      anchorEl={anchorEl}
      open={open}
      onClose={handleClose}
      MenuListProps={{
        "aria-labelledby": "settings-button",
      }}
      anchorOrigin={{
        vertical: "bottom",
        horizontal: "right",
      }}
      transformOrigin={{
        vertical: "top",
        horizontal: "right",
      }}
    >
      <ListItem sx={{ py: 1.5, pr: 20 }}>
        <Typography variant="subtitle2" color="grey.600">
          View Settings
        </Typography>
      </ListItem>
      <Divider />
      <MenuList>
        <MenuItem>
          <ListItemIcon>
            <SortByIcon />
          </ListItemIcon>
          <Box
            display="flex"
            flexDirection="row"
            width="100%"
            justifyContent="space-between"
          >
            <Typography variant="h5" color="grey.500" mr={1.5}>
              Sort by
            </Typography>

            <Typography variant="h5" color="primary.main">
              Number of proper citation
            </Typography>
          </Box>
          <ChevronRightIcon
            fontSize="small"
            color="primary"
            viewBox="0 -4.5 30 30 "
          />
        </MenuItem>

        <MenuItem>
          <ListItemIcon>
            <ViewLayoutIcon />
          </ListItemIcon>
          <Box
            display="flex"
            flexDirection="row"
            width="100%"
            justifyContent="space-between"
          >
            <Typography variant="h5" color="grey.500" mr={1.5}>
              View
            </Typography>

            <Typography variant="h5" color="primary.main">
              All Results
            </Typography>
          </Box>
          <ChevronRightIcon
            fontSize="small"
            color="primary"
            viewBox="0 -4.5 30 30 "
          />
        </MenuItem>
        <Divider />
        <MenuItem>
          <GridToolbarColumnsButton />
        </MenuItem>
      </MenuList>
    </Menu>
  );
};

export default TableSettingsMenu;
