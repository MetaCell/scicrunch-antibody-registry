import * as React from "react";
import SvgIcon, { SvgIconProps } from "@mui/material/SvgIcon";

export const HelpIcon = (props: SvgIconProps) => (
  <SvgIcon viewBox="-3 -3 26 26" {...props}>
    <path
      d="M7.57533 7.49984C7.77125 6.94289 8.15795 6.47326 8.66695 6.17411C9.17596 5.87497 9.77441 5.76562 10.3563 5.86543C10.9382 5.96524 11.466 6.26777 11.8462 6.71944C12.2264 7.17111 12.4345 7.74277 12.4337 8.33317C12.4337 9.99984 9.93366 10.8332 9.93366 10.8332M10.0003 14.1665H10.0087M18.3337 9.99984C18.3337 14.6022 14.6027 18.3332 10.0003 18.3332C5.39795 18.3332 1.66699 14.6022 1.66699 9.99984C1.66699 5.39746 5.39795 1.6665 10.0003 1.6665C14.6027 1.6665 18.3337 5.39746 18.3337 9.99984Z"
      stroke="#98A2B3"
      strokeWidth="1.66667"
      strokeLinecap="round"
      strokeLinejoin="round"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    />
  </SvgIcon>
);

export const SearchIcon = (props: SvgIconProps) => (
  <SvgIcon viewBox="0 0 18 18" {...props}>
    <path
      d="M16.5 16.5L11.5001 11.5M13.1667 7.33333C13.1667 10.555 10.555 13.1667 7.33333 13.1667C4.11167 13.1667 1.5 10.555 1.5 7.33333C1.5 4.11167 4.11167 1.5 7.33333 1.5C10.555 1.5 13.1667 4.11167 13.1667 7.33333Z"
      stroke="#98A2B3"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    />
  </SvgIcon>
);

export const SlashIcon = (props: SvgIconProps) => (
  <SvgIcon viewBox="0 0 16 16" {...props}>
    <path
      d="M4.66699 14.6668L11.3337 1.3335"
      stroke="#98A2B3"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </SvgIcon>
);

export const AddAntibodyIcon = (props: SvgIconProps) => (
  <SvgIcon fontSize="small" viewBox="0 0 14 14" {...props}>
    <path
      d="M7.00033 1.1665V12.8332M1.16699 6.99984H12.8337"
      stroke="white"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      fill="none"
    />
  </SvgIcon>
);

export const DownloadIcon = (props: SvgIconProps) => (
  <SvgIcon fontSize="small" viewBox="0 0 20 20" {...props}>
    <path
      d="M6.66699 9.99984L10.0003 13.3332M10.0003 13.3332L13.3337 9.99984M10.0003 13.3332V6.6665M18.3337 9.99984C18.3337 14.6022 14.6027 18.3332 10.0003 18.3332C5.39795 18.3332 1.66699 14.6022 1.66699 9.99984C1.66699 5.39746 5.39795 1.6665 10.0003 1.6665C14.6027 1.6665 18.3337 5.39746 18.3337 9.99984Z"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      fill="none"
    />
  </SvgIcon>
);

export const HouseIcon = (props: SvgIconProps) => (
  <SvgIcon
    fontSize="small"
    viewBox="0 0 20 20"
    strokeWidth="1.5"
    strokeLinecap="round"
    strokeLinejoin="round"
    {...props}
  >
    <path
      d="M6.66667 14.1668H13.3333M9.18141 2.30345L3.52949 6.69939C3.15168 6.99324 2.96278 7.14017 2.82669 7.32417C2.70614 7.48716 2.61633 7.67077 2.56169 7.866C2.5 8.08639 2.5 8.3257 2.5 8.80433V14.8334C2.5 15.7669 2.5 16.2336 2.68166 16.5901C2.84144 16.9037 3.09641 17.1587 3.41002 17.3185C3.76654 17.5001 4.23325 17.5001 5.16667 17.5001H14.8333C15.7668 17.5001 16.2335 17.5001 16.59 17.3185C16.9036 17.1587 17.1586 16.9037 17.3183 16.5901C17.5 16.2336 17.5 15.7669 17.5 14.8334V8.80433C17.5 8.3257 17.5 8.08639 17.4383 7.866C17.3837 7.67077 17.2939 7.48716 17.1733 7.32417C17.0372 7.14017 16.8483 6.99324 16.4705 6.69939L10.8186 2.30345C10.5258 2.07574 10.3794 1.96189 10.2178 1.91812C10.0752 1.87951 9.92484 1.87951 9.78221 1.91812C9.62057 1.96189 9.47418 2.07574 9.18141 2.30345Z"
      fill="none"
    />
  </SvgIcon>
);

export const SendIcon = (props: SvgIconProps) => (
  <SvgIcon
    fontSize="small"
    viewBox="0 0 18 18"
    strokeWidth="1.5"
    strokeLinecap="round"
    strokeLinejoin="round"
    {...props}
  >
    <path
      d="M7.74928 10.2501L16.4993 1.50014M7.85559 10.5235L10.0457 16.1552C10.2386 16.6513 10.3351 16.8994 10.4741 16.9718C10.5946 17.0346 10.7381 17.0347 10.8587 16.972C10.9978 16.8998 11.0946 16.6518 11.2881 16.1559L16.78 2.08281C16.9547 1.63516 17.0421 1.41133 16.9943 1.26831C16.9528 1.1441 16.8553 1.04663 16.7311 1.00514C16.5881 0.957356 16.3643 1.0447 15.9166 1.21939L1.84349 6.71134C1.34759 6.90486 1.09965 7.00163 1.02739 7.14071C0.964749 7.26129 0.964833 7.40483 1.02761 7.52533C1.10004 7.66433 1.3481 7.7608 1.84422 7.95373L7.47589 10.1438C7.5766 10.183 7.62695 10.2026 7.66935 10.2328C7.70693 10.2596 7.7398 10.2925 7.7666 10.3301C7.79685 10.3725 7.81643 10.4228 7.85559 10.5235Z"
      fill="none"
    />
  </SvgIcon>
);

export const FilteringIcon = (props: SvgIconProps) => (
  <SvgIcon
    width="20"
    height="20"
    viewBox="0 0 20 20"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    stroke="#667085"
    strokeWidth="1.66667"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d="M5 10H15M2.5 5H17.5M7.5 15H12.5" />
  </SvgIcon>
);

export const SettingsIcon = (props: SvgIconProps) => (
  <SvgIcon
    width="20"
    height="20"
    viewBox="0 0 20 20"
    xmlns="http://www.w3.org/2000/svg"
    stroke="#667085"
    strokeWidth="1.66667"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path
      d="M2.5 6.6665L12.5 6.6665M12.5 6.6665C12.5 8.04722 13.6193 9.1665 15 9.1665C16.3807 9.1665 17.5 8.04722 17.5 6.6665C17.5 5.28579 16.3807 4.1665 15 4.1665C13.6193 4.1665 12.5 5.28579 12.5 6.6665ZM7.5 13.3332L17.5 13.3332M7.5 13.3332C7.5 14.7139 6.38071 15.8332 5 15.8332C3.61929 15.8332 2.5 14.7139 2.5 13.3332C2.5 11.9525 3.61929 10.8332 5 10.8332C6.38071 10.8332 7.5 11.9525 7.5 13.3332Z"
      fill="none"
    />
  </SvgIcon>
);

export const CheckedIcon = (props: SvgIconProps) => (
  <SvgIcon
    sx={{ height: "1.25rem", width: "1.25rem" }}
    viewBox="0 0 20 20"
    xmlns="http://www.w3.org/2000/svg"
  >
    <rect
      x="0.5"
      y="0.5"
      width="19"
      height="19"
      rx="5.5"
      stroke="#2173F2"
      fill="none"
    />
    <path
      d="M14.6666 6.5L8.24992 12.9167L5.33325 10"
      stroke="#2173F2"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      fill="none"
    />
  </SvgIcon>
);

export const UncheckedIcon = (props: SvgIconProps) => (
  <SvgIcon
    sx={{ height: "1.25rem", width: "1.25rem" }}
    viewBox="0 0 20 20"
    xmlns="http://www.w3.org/2000/svg"
  >
    <rect
      x="0.5"
      y="0.5"
      width="19px"
      height="19px"
      rx="5.5"
      stroke="#D0D5DD"
      fill="white"
    />
  </SvgIcon>
);

export const FilteredColumnIcon = (props: SvgIconProps) => (
  <SvgIcon
    sx={{ width: "1.1rem", height: "1.1rem" }}
    viewBox="0 0 16 16"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <g clip-path="url(#clip0_801_17210)">
      <path
        d="M4 8H12M2 4H14M6 12H10"
        stroke="#667085"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <circle
        cx="13"
        cy="3"
        r="3.75"
        fill="#2173F2"
        stroke="#F9FAFB"
        strokeWidth="1.5"
      />
    </g>
    <defs>
      <clipPath id="clip0_801_17210">
        <rect width="16" height="16" fill="white" />
      </clipPath>
    </defs>
  </SvgIcon>
);

export const SortingIcon = (props: SvgIconProps) => (
  <SvgIcon
    sx={{ height: "0.75rem", width: "0.5rem " }}
    viewBox="0 0 8 12"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M0.666748 7.99984L4.00008 11.3332L7.33341 7.99984"
      fill="#98A2B3"
    />
    <path
      d="M0.666748 3.99984L4.00008 0.666504L7.33341 3.99984"
      fill="#98A2B3"
    />
  </SvgIcon>
);

export const AscSortedIcon = (props: SvgIconProps) => (
  <SvgIcon
    sx={{ height: "0.75rem", width: "0.5rem " }}
    viewBox="0 0 8 12"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M0.666748 7.99984L4.00008 11.3332L7.33341 7.99984"
      fill="#98A2B3"
    />
    <path
      d="M0.666748 3.99984L4.00008 0.666504L7.33341 3.99984"
      // TODO: change fill color with the right one
      fill="#475467"
    />
  </SvgIcon>
);

export const DescSortedIcon = (props: SvgIconProps) => (
  <SvgIcon
    sx={{ height: "0.75rem", width: "0.5rem " }}
    viewBox="0 0 8 12"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M0.666748 7.99984L4.00008 11.3332L7.33341 7.99984"
      // TODO: change fill color with the right one
      fill="#475467"
    />
    <path
      d="M0.666748 3.99984L4.00008 0.666504L7.33341 3.99984"
      fill="#98A2B3"
    />
  </SvgIcon>
);

export const FaqIcon = (props: SvgIconProps) => (
  <SvgIcon viewBox="0 -6 28 24" fill="none">
    <path
      d="M13 5.99968L5 5.99967M13 1.99968L5 1.99967M13 9.99968L5 9.99967M2.33333 5.99967C2.33333 6.36786 2.03486 6.66634 1.66667 6.66634C1.29848 6.66634 1 6.36786 1 5.99967C1 5.63148 1.29848 5.33301 1.66667 5.33301C2.03486 5.33301 2.33333 5.63148 2.33333 5.99967ZM2.33333 1.99967C2.33333 2.36786 2.03486 2.66634 1.66667 2.66634C1.29848 2.66634 1 2.36786 1 1.99967C1 1.63148 1.29848 1.33301 1.66667 1.33301C2.03486 1.33301 2.33333 1.63148 2.33333 1.99967ZM2.33333 9.99967C2.33333 10.3679 2.03486 10.6663 1.66667 10.6663C1.29848 10.6663 1 10.3679 1 9.99967C1 9.63148 1.29848 9.33301 1.66667 9.33301C2.03486 9.33301 2.33333 9.63148 2.33333 9.99967Z"
      stroke="#667085"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </SvgIcon>
);

export const EmailIcon = (props: SvgIconProps) => (
  <SvgIcon viewBox="0 -6 28 24" fill="none">
    <path
      d="M14.333 11.0003L9.90444 7.00033M6.09491 7.00033L1.66636 11.0003M1.33301 3.66699L6.77629 7.47729C7.21707 7.78583 7.43746 7.94011 7.67718 7.99986C7.88894 8.05265 8.11041 8.05265 8.32217 7.99986C8.56189 7.94011 8.78228 7.78583 9.22306 7.47729L14.6663 3.66699M4.53301 12.3337H11.4663C12.5864 12.3337 13.1465 12.3337 13.5743 12.1157C13.9506 11.9239 14.2566 11.618 14.4484 11.2416C14.6663 10.8138 14.6663 10.2538 14.6663 9.13366V4.86699C14.6663 3.74689 14.6663 3.18683 14.4484 2.75901C14.2566 2.38269 13.9506 2.07673 13.5743 1.88498C13.1465 1.66699 12.5864 1.66699 11.4663 1.66699H4.53301C3.4129 1.66699 2.85285 1.66699 2.42503 1.88498C2.0487 2.07673 1.74274 2.38269 1.55099 2.75901C1.33301 3.18683 1.33301 3.74689 1.33301 4.86699V9.13366C1.33301 10.2538 1.33301 10.8138 1.55099 11.2416C1.74274 11.618 2.0487 11.9239 2.42503 12.1157C2.85285 12.3337 3.4129 12.3337 4.53301 12.3337Z"
      stroke="#667085"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      fill="none"
    />
  </SvgIcon>
);

export const InfoIcon = (props: SvgIconProps) => (
  <SvgIcon viewBox="0 -5.5 28 24" fill="none">
    <path
      d="M7 9.66667V7M7 4.33333H7.00667M4.2 13H9.8C10.9201 13 11.4802 13 11.908 12.782C12.2843 12.5903 12.5903 12.2843 12.782 11.908C13 11.4802 13 10.9201 13 9.8V4.2C13 3.0799 13 2.51984 12.782 2.09202C12.5903 1.71569 12.2843 1.40973 11.908 1.21799C11.4802 1 10.9201 1 9.8 1H4.2C3.0799 1 2.51984 1 2.09202 1.21799C1.71569 1.40973 1.40973 1.71569 1.21799 2.09202C1 2.51984 1 3.0799 1 4.2V9.8C1 10.9201 1 11.4802 1.21799 11.908C1.40973 12.2843 1.71569 12.5903 2.09202 12.782C2.51984 13 3.0799 13 4.2 13Z"
      stroke="#667085"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      fill="none"
    />
  </SvgIcon>
);

export const FilterIcon = (props: SvgIconProps) => (
  <SvgIcon viewBox="-3 -2.5 21 15" fill="none" fontSize="small">
    <path
      d="M3 5H11M1 1H13M5 9H9"
      stroke="#667085"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </SvgIcon>
);

export const SortByIcon = (props: SvgIconProps) => (
  <SvgIcon viewBox="-5 -5 24 24" fill="none" fontSize="small">
    <path
      d="M10.3333 1.66699V12.3337M10.3333 12.3337L7.66667 9.66699M10.3333 12.3337L13 9.66699M3.66667 12.3337V1.66699M3.66667 1.66699L1 4.33366M3.66667 1.66699L6.33333 4.33366"
      stroke="#667085"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </SvgIcon>
);

export const ViewLayoutIcon = (props: SvgIconProps) => (
  <SvgIcon viewBox="-5 -5 23 23" fill="none" fontSize="small">
    <path
      d="M1 5H13M5 5L5 13M4.2 1H9.8C10.9201 1 11.4802 1 11.908 1.21799C12.2843 1.40973 12.5903 1.71569 12.782 2.09202C13 2.51984 13 3.0799 13 4.2V9.8C13 10.9201 13 11.4802 12.782 11.908C12.5903 12.2843 12.2843 12.5903 11.908 12.782C11.4802 13 10.9201 13 9.8 13H4.2C3.07989 13 2.51984 13 2.09202 12.782C1.71569 12.5903 1.40973 12.2843 1.21799 11.908C1 11.4802 1 10.9201 1 9.8V4.2C1 3.07989 1 2.51984 1.21799 2.09202C1.40973 1.71569 1.71569 1.40973 2.09202 1.21799C2.51984 1 3.0799 1 4.2 1Z"
      stroke="#667085"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      fill="none"
    />
  </SvgIcon>
);

export const BackIcon = (props: SvgIconProps) => (
  <SvgIcon viewBox="0 0 17 13" fontSize="small">
    <path
      d="M1 4.49996H12.25C14.3211 4.49996 16 6.17889 16 8.24996C16 10.321 14.3211 12 12.25 12H8.5M1 4.49996L4.33333 1.16663M1 4.49996L4.33333 7.83329"
      stroke="#667085"
      strokeWidth="1.66667"
      strokeLinecap="round"
      strokeLinejoin="round"
      fill="none"
    />
  </SvgIcon>
);

export const StepIcon = (props: SvgIconProps) => (
  <SvgIcon viewBox="0 0 17 13" fontSize="small">
    <rect width="24" height="24" rx="12" fill="#DFEBF8" />
    <circle cx="12" cy="12" r="4" fill="#2173F2" />
  </SvgIcon>
);

export const CopyIcon = (props: SvgIconProps) => (
  <SvgIcon viewBox="0 0 20 20" fontSize="small" stroke={props.stroke}>
    <path
      d="M4.16699 12.5C3.39042 12.5 3.00214 12.5 2.69585 12.3731C2.28747 12.2039 1.96302 11.8795 1.79386 11.4711C1.66699 11.1648 1.66699 10.7765 1.66699 9.99996V4.33329C1.66699 3.39987 1.66699 2.93316 1.84865 2.57664C2.00844 2.26304 2.2634 2.00807 2.57701 1.84828C2.93353 1.66663 3.40024 1.66663 4.33366 1.66663H10.0003C10.7769 1.66663 11.1652 1.66663 11.4715 1.79349C11.8798 1.96265 12.2043 2.28711 12.3735 2.69549C12.5003 3.00177 12.5003 3.39006 12.5003 4.16663M10.167 18.3333H15.667C16.6004 18.3333 17.0671 18.3333 17.4236 18.1516C17.7372 17.9918 17.9922 17.7369 18.152 17.4233C18.3337 17.0668 18.3337 16.6 18.3337 15.6666V10.1666C18.3337 9.23321 18.3337 8.7665 18.152 8.40998C17.9922 8.09637 17.7372 7.8414 17.4236 7.68162C17.0671 7.49996 16.6004 7.49996 15.667 7.49996H10.167C9.23357 7.49996 8.76686 7.49996 8.41034 7.68162C8.09674 7.8414 7.84177 8.09637 7.68198 8.40998C7.50033 8.7665 7.50033 9.23321 7.50033 10.1666V15.6666C7.50033 16.6 7.50033 17.0668 7.68198 17.4233C7.84177 17.7369 8.09674 17.9918 8.41034 18.1516C8.76686 18.3333 9.23357 18.3333 10.167 18.3333Z"
      strokeWidth="1.66667"
      strokeLinecap="round"
      strokeLinejoin="round"
      fill="none"
    />
  </SvgIcon>
);

export const ExternalLinkIcon = (props: SvgIconProps) => (
  <SvgIcon viewBox="0 0 20 20" fontSize="small" stroke={props.stroke}>
    <path
      d="M16.5 6.50001L16.5 1.50001M16.5 1.50001H11.5M16.5 1.50001L9 9M7.33333 1.5H5.5C4.09987 1.5 3.3998 1.5 2.86502 1.77248C2.39462 2.01217 2.01217 2.39462 1.77248 2.86502C1.5 3.3998 1.5 4.09987 1.5 5.5V12.5C1.5 13.9001 1.5 14.6002 1.77248 15.135C2.01217 15.6054 2.39462 15.9878 2.86502 16.2275C3.3998 16.5 4.09987 16.5 5.5 16.5H12.5C13.9001 16.5 14.6002 16.5 15.135 16.2275C15.6054 15.9878 15.9878 15.6054 16.2275 15.135C16.5 14.6002 16.5 13.9001 16.5 12.5V10.6667"
      strokeWidth="1.66667"
      strokeLinecap="round"
      strokeLinejoin="round"
      fill="none"
    />
  </SvgIcon>
);
