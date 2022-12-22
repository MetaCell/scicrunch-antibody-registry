
import {
  UsersApi, 
  User as ApiUser,
} from "../rest/accounts-api/api";
import { createContext } from "react";

import { Configuration } from "../rest/accounts-api";

export const UserContext = createContext(null);
const getUserApi = () => new UsersApi(new Configuration({ apiKey: getToken(), accessToken: getToken(), basePath: "/proxy/accounts-api/api" }));

export interface User extends ApiUser{
  preferredUsername?: string;
  realmAccess?: {roles: string[]};
}

function getCookie(name): string {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(";").shift();
  }
  return null;
}

export async function fetchUser(userId): Promise<User> {
  return getUserApi().getUser(userId);
}

function mapUser(jwtUser: any): User {
  return jwtUser && {
    ...jwtUser,
    firstName: jwtUser.given_name,
    lastName: jwtUser.family_name,
    preferredUsername: jwtUser.preferred_username,
    realmAccess: jwtUser.realm_access,
  };
}

function parseJwt(token: string): User {
  if (!token) {
    return null;
  }
  const base64Url: string = token.split(".")[1];
  const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
  const jsonPayload = decodeURIComponent(
    window
      .atob(base64)
      .split("")
      .map((c) => {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join("")
  );

  return JSON.parse(jsonPayload);
}


export function getCurrentUserFromCookie() {
  return mapUser(parseJwt(getToken()));
}

export async function updateUser(user: User) {
  return getUserApi().updateUser(getCurrentUserFromCookie().sub, user, );
}


export async function updateUserPassword(oldPassword: string, newPassword: string) {
  return getUserApi().usersUsernamePasswordPut(getCurrentUserFromCookie().preferredUsername, { old_password: oldPassword, new_password: newPassword });
}

export async function associateOrcid(orcid: string) {
  return getUserApi().usersUsernameOrcidPut(getCurrentUserFromCookie().sub,  orcid );
}



export function getToken(): string {
  return getCookie("kc-access");
}

