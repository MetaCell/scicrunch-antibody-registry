import React from "react";
import { useTheme } from "@mui/material/styles";
import {
  Grid,
  Typography,
  Button,
  Box,
  Divider,
  TextField,
  InputAdornment,
  Alert,
} from "@mui/material";
import { CheckIcon, EmailIcon } from "../icons";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import VisibilityOffOutlinedIcon from "@mui/icons-material/VisibilityOffOutlined";
import * as  UserService from "../../services/UserService";

import { User } from "../../services/UserService";

interface UserProps {
  user: User;
}

const AccountDetailsForm = (props: UserProps) => {
  const theme = useTheme();
  const [isPassOrigShown, setIsPassOrigShown] = React.useState(false);
  const [isPassNewShown, setIsPassNewShown] = React.useState(false);
  const [isPassConfirmShown, setIsPassConfirmShown] = React.useState(false);

  const [user, setUser] = React.useState<User>({ firstName: props.user.firstName, lastName: props.user.lastName, email: props.user.email, orcid: props.user.orcid });

  const [passwordOrig, setPasswordOrig] = React.useState("");
  const [passwordNew, setPasswordNew] = React.useState("");
  const [passwordConfirm, setPasswordConfirm] = React.useState("");
  const [orcid, setOrcid] = React.useState<string>(props.user.orcid || "");
  const [orcidMsg, setOrcidMsg] = React.useState<string>("");

  const [updateResult, setUpdateResult] = React.useState<Boolean|string>(null);

  const styles = {
    saveButton: {
      border: `1px solid ${theme.palette.primary.contrastText}`,
      boxShadow:
        "0px 1px 2px rgba(16, 24, 40, 0.05), inset 0px -2px 0px rgba(255, 255, 255, 0.25)",
      "&.Mui-disabled": {
        color: "white",
        backgroundColor: theme.palette.primary.contrastText,
      },
    },
    orcidButton: {
      border: `1px solid ${theme.palette.grey[300]}`,
      height: "2.5rem",
    },
    showButton: {
      color: theme.palette.grey[700],
      borderRadius: "0px 8px 8px 0px",
      height: "2.5rem",
      borderLeft: `1px solid ${theme.palette.grey[300]}`,
      padding: "1rem",
    },
    main: {
      "& .MuiInputBase-root.MuiOutlinedInput-root": {
        height: "2.5rem",
        padding: 0,
      },
    },
  };

  const saveUser = () => {
    UserService.updateUser({ ...user }).then((res) => {
      console.log(res);
    });
    if(passwordNew && passwordConfirm && passwordOrig && !passwordError) {
      UserService.updateUserPassword(passwordOrig, passwordNew).then(() => {
        setUpdateResult(true);
      }, (res) => {
        console.error(res)
        setUpdateResult(res);
      });
    }
  }

  const handleOrigPasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPasswordOrig(event.target.value);
  }

  const handleConfirmPasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPasswordConfirm(event.target.value);
  }
  const handleNewPasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPasswordNew(event.target.value);
  }

  const passwordError = Boolean(passwordNew !== passwordConfirm && passwordNew && passwordConfirm);


  function handleAssociateOrcid(): void {
    setOrcidMsg("ORCID association failed: TBD");
    
  }

  return (
    <form>
      <Grid container p={3} gap={3} direction="column" sx={styles.main}>
        <Grid
          item
          display="flex"
          p={0}
          justifyContent="space-between"
          textAlign="left"
        >
          <div>
            <Typography variant="h2" color="grey.900" pb={0.5}>
              Account details
            </Typography>
            <Typography variant="subtitle1" color="grey.500">
              Update your personal details.
            </Typography>
          </div>
          <Button
            variant="contained"
            startIcon={<CheckIcon />}
            disabled={Boolean(passwordError || ((!passwordConfirm || !passwordNew) && passwordOrig))}
            sx={styles.saveButton}
            onClick={saveUser}
          >
            Save changes
          </Button>
        </Grid>
        <Divider />
        {updateResult === true && <Alert severity="info">Password updated successfully</Alert>}
        {updateResult !== true && updateResult !== null && <Alert severity="error"><>Password update failed</></Alert>}
        <Grid item p={0} textAlign="left" display="flex" gap={4}>
          <Grid item lg={3}>
            <Typography color="grey.500">Personal details</Typography>
          </Grid>
          <Grid item lg={9} display="flex" justifyContent="space-between">
            <Grid item lg={5.9}>
              <Typography variant="subtitle1" color="grey.700" pb={0.75}>
                First Name
              </Typography>
              <TextField 
                value={user.firstName} 
                fullWidth 
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setUser({ ...user, firstName: e.target.value })} />
            </Grid>
            <Grid item lg={5.9}>
              <Typography variant="subtitle1" color="grey.700" pb={0.75}>
                Last Name
              </Typography>
              <TextField value={user.lastName} 
                fullWidth 
                
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setUser({ ...user, lastName: e.target.value })}
                
              />
            </Grid>
          </Grid>
        </Grid>
        <Divider />
        <Grid item p={0} textAlign="left" display="flex" gap={4}>
          <Grid item lg={3}>
            <Typography color="grey.500">Email</Typography>
            <Typography variant="subtitle1" color="grey.500">
              This is your login credential and the email address used for
              password recovering.
            </Typography>
          </Grid>
          <Grid item lg={9}>
            <Typography variant="subtitle1" color="grey.700" pb={0.75}>
              Email
            </Typography>
            <TextField
              fullWidth
              value={props.user.email}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start" sx={{ pl: 2 }}>
                    <EmailIcon />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
        </Grid>
        <Divider />
        <Grid item p={0} textAlign="left" display="flex" gap={4}>
          <Grid item lg={3}>
            <Typography color="grey.500">Password</Typography>
            <Typography variant="subtitle1" color="grey.500">
              Update your password.
            </Typography>
          </Grid>
          <Grid item lg={9} columnSpacing={2}>
            <Box pb={2}>
              <Typography variant="subtitle1" color="grey.700" pb={0.75}>
                Original password
              </Typography>
              <TextField
                fullWidth
                type={isPassOrigShown ? "text" : "password"}
                placeholder="Type your original password"
                onChange={handleOrigPasswordChange}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <Button
                        startIcon={
                          isPassOrigShown ? (
                            <VisibilityOffOutlinedIcon sx={{ color: "#000" }} />
                          ) : (
                            <VisibilityOutlinedIcon sx={{ color: "#000" }} />
                          )
                        }
                        sx={styles.showButton}
                        color="inherit"
                        onClick={() => setIsPassOrigShown(!isPassOrigShown)}
                      >
                        Show
                      </Button>
                    </InputAdornment>
                  ),
                }}
              />
            </Box>
            <Box pb={2}>
              <Typography variant="subtitle1" color="grey.700" pb={0.75}>
                New password
              </Typography>
              <TextField
                fullWidth
                placeholder="Create a new password"
                type={isPassNewShown ? "text" : "password"}
                onChange={handleNewPasswordChange}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <Button
                        startIcon={
                          isPassNewShown ? (
                            <VisibilityOffOutlinedIcon sx={{ color: "#000" }} />
                          ) : (
                            <VisibilityOutlinedIcon sx={{ color: "#000" }} />
                          )
                        }
                        sx={styles.showButton}
                        color="inherit"
                        onClick={() => setIsPassNewShown(!isPassNewShown)}
                      >
                        Show
                      </Button>
                    </InputAdornment>
                  ),
                }}
              />
            </Box>
            <Box pb={2}>
              <Typography variant="subtitle1" color="grey.700" pb={0.75}>
                Confirm password
              </Typography>
              <TextField
                fullWidth
                placeholder="Confirm your new password"
                error={passwordError} 
                type={isPassConfirmShown ? "text" : "password"}
                onChange={handleConfirmPasswordChange}
                helperText={passwordError ? "Passwords do not match" : ""}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <Button
                        startIcon={
                          isPassConfirmShown ? (
                            <VisibilityOffOutlinedIcon sx={{ color: "#000" }} />
                          ) : (
                            <VisibilityOutlinedIcon sx={{ color: "#000" }} />
                          )
                        }
                        sx={styles.showButton}
                        color="inherit"
                        onClick={() =>
                          setIsPassConfirmShown(!isPassConfirmShown)
                        }
                      >
                        Show
                      </Button>
                    </InputAdornment>
                  ),
                }}
              />
            </Box>
          </Grid>
        </Grid>
        <Divider />
        {orcidMsg && <Alert severity={orcidMsg.includes("fail") ? "error": "info"}>{orcidMsg}</Alert>}
        <Grid item p={0} textAlign="left" display="flex" gap={4}>
          <Grid item lg={3}>
            <Typography color="grey.500">ORCID ID</Typography>
            <Typography variant="subtitle1" color="grey.500">
              You can associate your ORCID ID to your account.
            </Typography>
          </Grid>

          
          <Grid item lg={9} columnSpacing={2} justifyContent="space-between" display="flex">
            <TextField 
              value={orcid} 
              sx={{ pr: 2, flex: 1 }}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setOrcid(e.target.value)} />
          
          
            {<Button
              variant="outlined"
              color="inherit"
              sx={styles.orcidButton}
              onClick={handleAssociateOrcid}
            >
            Associate ORCID ID
            </Button>
            }
          </Grid>
        </Grid>
      </Grid>
    </form>
  );
};
export default AccountDetailsForm;
