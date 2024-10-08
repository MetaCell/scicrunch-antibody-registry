import React from "react";
import { Link } from "react-router-dom"
import { useHistory } from "react-router-dom"
import {
  IconButton,
  Menu,
  ListItem,
  ListItemIcon,
  Typography,
  Divider,
  MenuList,
  MenuItem,
  Stack
} from "@mui/material";
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';

import { ThreeDotsIcon, UserIcon, LogoutIcon, CubeIcon } from "../icons";

import { User } from "../../services/UserService"

interface UserProps {
    user: User
}

const UserAccountMenu = (props: UserProps) => {
  const { user } = props;
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const history = useHistory();
  const open = Boolean(anchorEl);


  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  return (<>
    <Stack direction="row" spacing={1} className="user-menu">
      <div>
        <Typography variant="subtitle1" align="left" sx={{
          color: "grey.400"
        }}>Account</Typography>
        <Typography variant="subtitle2" align="left" sx={{
          color: "grey.700"
        }}>{user.firstName ? `${user.firstName} ${user.lastName}` : user.email}</Typography>
      </div>
      <IconButton
        disableRipple
        className="btn-user-menu"
        sx={{
          p: 1.25,
        }}
        onClick={handleClick}
        aria-controls={open ? 'account-menu' : undefined}
        aria-haspopup="true"
        aria-expanded={open ? 'true' : undefined}
      >
        <ThreeDotsIcon />
      </IconButton>
    </Stack>
    <Menu
      anchorEl={anchorEl}
      id="account-menu"
      open={open}
      onClose={handleClose}
      MenuListProps={{
        "aria-labelledby": "help-button",
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
        <Stack spacing={0}>
          <Typography variant="subtitle2" sx={{
            color: "grey.600"
          }}>
            {user.firstName ? `${user.firstName} ${user.lastName}` : user?.preferredUsername}
          </Typography>
          <Typography variant="subtitle1" sx={{
            color: "grey.400"
          }}>
            {user.email}
          </Typography>
        </Stack>
      </ListItem>
      <Divider />
      <MenuList sx={{ "& .MuiMenuItem-root": { paddingTop: "0.4rem" } }}>
        <MenuItem className="btn-account-details" onClick={() => {
          history.push("/user"); setAnchorEl(null)}} component={Link}>
          <ListItemIcon>
            <UserIcon />
          </ListItemIcon>
          <Typography variant="h5" sx={{
            color: "grey.500"
          }}>Account details</Typography>
        </MenuItem>
        {/* <MenuItem>
          <ListItemIcon>
            <CubeIcon />
          </ListItemIcon>
          <Typography variant="h5" color="grey.500">API Key</Typography>
        </MenuItem> */}
        {user.realmAccess.roles.includes("administrator") && <MenuItem className="btn-admin-panel" onClick={() => window.location.href = "/admin/"}>
          <ListItemIcon>
            <AdminPanelSettingsIcon fontSize="small" sx={{ pl: 0 }}  />
          </ListItemIcon>
          <Typography variant="h5" sx={{
            color: "grey.500"
          }}>Admin panel</Typography>
        </MenuItem> }
        <Divider />
        <MenuItem className="btn-logout" onClick={() => 
          fetch("/oauth/logout").then(() => window.location.href = "/", () => window.location.href = "/oauth/logout")
        }>
          <ListItemIcon>
            <LogoutIcon />
          </ListItemIcon>
          <Typography variant="h5" sx={{
            color: "grey.500"
          }}>Log out</Typography>
        </MenuItem>
      </MenuList>
    </Menu>
  </>);
}
export default UserAccountMenu;