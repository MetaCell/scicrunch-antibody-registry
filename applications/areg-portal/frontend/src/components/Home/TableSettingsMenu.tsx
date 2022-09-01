import React from "react";
import {
  IconButton,
  Menu,
  MenuList,
  MenuItem,
  ListItem,
  ListItemIcon,
  Typography,
  Divider,
} from "@mui/material";

import { GridToolbarColumnsButton } from "@mui/x-data-grid";

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
          <Typography variant="h5" color="grey.500">
            Sort by
          </Typography>
        </MenuItem>

        <MenuItem>
          <Typography variant="h5" color="grey.500">
            View
          </Typography>
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
