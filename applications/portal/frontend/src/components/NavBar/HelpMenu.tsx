import React from "react";
import { Link } from "react-router-dom"
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
import { HelpIcon, FaqIcon, EmailIcon, InfoIcon } from "../icons";
import Handshake from '@mui/icons-material/Handshake';

const HelpMenu = () => {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  return (<>
    <IconButton
      disableRipple
      sx={{
        p: 1.25,
      }}
      id="help-button"
      aria-controls={open ? "help-menu" : undefined}
      aria-haspopup="true"
      aria-expanded={open ? "true" : undefined}
      onClick={handleClick}
      className="btn-help-menu"
    >
      <HelpIcon />
    </IconButton>
    <Menu
      id="help-menu"
      anchorEl={anchorEl}
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
        <Typography variant="subtitle2" sx={{
          color: "grey.600"
        }}>
          Help and support
        </Typography>
      </ListItem>
      <Divider />
      <MenuList>
        <MenuItem className="link-faq" component={Link} to="/faq" onClick={handleClose}>
          <ListItemIcon>
            <FaqIcon />
          </ListItemIcon>
          <Typography variant="h5" sx={{
            color: "grey.500"
          }}>
            FAQ
          </Typography>
        </MenuItem>
        <MenuItem className="link-membership" component={Link} to="/membership" onClick={handleClose}>
          <ListItemIcon>
            <Handshake fontSize="inherit" />
          </ListItemIcon>
          <Typography variant="h5" sx={{
            color: "grey.500"
          }}>
            Become a member
          </Typography>
        </MenuItem>

        <MenuItem className="link-contact" component="a" href="mailto:abr-help@scicrunch.org" >
          <ListItemIcon>
            <EmailIcon />
          </ListItemIcon>
          <Typography variant="h5" sx={{
            color: "grey.500"
          }}>
            Email us
          </Typography>
        </MenuItem>
        <Divider />
        <MenuItem className="link-terms-conditions" component={Link} to="/terms-and-conditions">
          <ListItemIcon>
            <InfoIcon />
          </ListItemIcon>
          <Typography
            variant="h5"
            sx={{
              color: "grey.500"
            }}
          >{`Terms & Conditions`}</Typography>
        </MenuItem>
      </MenuList>
    </Menu>
  </>);
};

export default HelpMenu;
