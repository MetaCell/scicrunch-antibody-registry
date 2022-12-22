import React, { useEffect, useState, useContext } from "react";
//MUI
import {
  DataGrid,
  useGridApiContext,
  GridColDef,
  GridRenderCellParams,
  GridCsvExportOptions,
  GridNoRowsOverlay,
} from "@mui/x-data-grid";
import {
  Typography,
  Box,
  Link,
  Checkbox,
  Popover,
  Button,
} from "@mui/material";
import { CopyToClipboard } from "react-copy-to-clipboard";

//project imports
import {
  getAntibodies,
  getUserAntibodies,
} from "../../services/AntibodiesService";
import {
  AscSortedIcon,
  DescSortedIcon,
  FilteredColumnIcon,
  SortingIcon,
  CheckedIcon,
  UncheckedIcon,
  FilterIcon,
  SettingsIcon,
  CopyIcon,
} from "../icons";
import HomeHeader from "./HomeHeader";
import { Antibody } from "../../rest";
import { getProperCitation } from "../../utils/antibody";
import { useTheme } from "@mui/system";
import { UserContext } from "../../services/UserService";
import ConnectAccount from "./ConnectAccount";
import { ALLRESULTS } from "../../constants/constants";
import SearchContext from "../../context/search/SearchContext";
import NotFoundMessage from "./NotFoundMessage";
import Error500 from "../UI/Error500";

const StyledBadge = (props) => {
  if (props.field === "vendorName") {
    return (
      <Box bgcolor="primary.light" px={0.5} py={0.25} borderRadius="0.25rem">
        <Link underline="none" target="_blank" href={props.row.url}>
          {props.children}
        </Link>
      </Box>
    );
  } else if (props.field === "clonality") {
    return (
      <Box bgcolor="grey.A200" px={1} py={0.25} borderRadius="1rem">
        {props.children}
      </Box>
    );
  } else {
    return <Box>{props.children}</Box>;
  }
};
const StyledCheckBox = (props) => {
  return (
    <Checkbox
      {...props}
      checkedIcon={<CheckedIcon />}
      icon={<UncheckedIcon />}
    />
  );
};

const getRowId = (ab: Antibody) => `${ab.abId}${Math.random()}`

const CustomToolbar = ({ activeTab }) => {
  const [activeSelection, setActiveSelection] = useState(true);

  const apiRef = useGridApiContext();
  const selectedRows = apiRef.current.getSelectedRows();

  const handleExport = (options: GridCsvExportOptions) =>
    apiRef.current.exportDataAsCsv(options);

  const showFilterMenu = () => apiRef.current.showFilterPanel();

  useEffect(() => {
    selectedRows.size === 0
      ? setActiveSelection(false)
      : setActiveSelection(true);
  }, [selectedRows]);

  return (
    <HomeHeader
      activeSelection={activeSelection}
      handleExport={handleExport}
      showFilterMenu={showFilterMenu}
      activeTab={activeTab}
    />
  );
};

const RenderNameAndId = (props: GridRenderCellParams<String>) => {
  return (
    <Link href ={`/AB_${props.row.abId}`}>
    
      <Typography
        variant="body2"
        align="left"
        color="grey.700"
        fontWeight={500}
      >
        {props.row.abName}
      </Typography>
      <Typography
        variant="caption"
        align="left"
        component="div"
        color="grey.500"
      >
        AB_{props.row.abId}
      </Typography>
    </Link>
  );
};

const RenderCellContent = (props: GridRenderCellParams<String>) => {
  return (
    <StyledBadge {...props}>
      <Typography
        variant="caption"
        align="left"
        color={props.field === "vendorName" ? "primary.main" : "grey.500"}
        component="div"
      >
        {props.field === "targetAntigen"
          ? `${props.row.abTarget} ${props.row.targetSpecies.join(", ")}`
          : props.value}
      </Typography>
    </StyledBadge>
  );
};


const RenderHtml= (props: GridRenderCellParams<String>) => {
  return (
    <StyledBadge {...props}>
      <Typography
        variant="caption"
        align="left"
        color="grey.500"
        component="div" 
        dangerouslySetInnerHTML={{ __html: props.value }}
      />
    </StyledBadge>
  );
};



const RenderProperCitation = (props: GridRenderCellParams<String>) => {
  const theme = useTheme();
  const classes = {
    popover: {
      p: 1,
      backgroundColor: theme.palette.grey[900],
      color: theme.palette.common.white,
      fontSize: "1rem",
    },

    citationColumn: {
      cursor: "auto",
      display: "flex",
      alignItems: "center",
    },
  };
  const [anchorCitationPopover, setAnchorCitationPopover] =
    useState<HTMLButtonElement | null>(null);

  const handleClickCitation = (event) => {
    setAnchorCitationPopover(event.currentTarget);
    setTimeout(handleCloseCitation, 1000);
  };

  const handleCloseCitation = () => {
    setAnchorCitationPopover(null);
  };

  const open = Boolean(anchorCitationPopover);
  const id = open ? "simple-popover" : undefined;
  return (
    <StyledBadge {...props}>
      <Box sx={classes.citationColumn}>
        <Typography
          variant="caption"
          align="left"
          color={props.field === "vendor" ? "primary.main" : "grey.500"}
          component="div"
        >
          {props.value}
        </Typography>
        <CopyToClipboard text={props.value}>
          <Button
            onClick={handleClickCitation}
            size="small"
            sx={{ minWidth: 0 }}
            startIcon={
              <CopyIcon stroke={theme.palette.grey[500]} fontSize="inherit" />
            }
          />
        </CopyToClipboard>
        <Popover
          id={id}
          open={open}
          anchorEl={anchorCitationPopover}
          onClose={handleCloseCitation}
          anchorOrigin={{
            vertical: "top",
            horizontal: "right",
          }}
          transformOrigin={{
            vertical: "center",
            horizontal: "center",
          }}
        >
          <Typography sx={classes.popover}>Citation copied</Typography>
        </Popover>
      </Box>
    </StyledBadge>
  );
};

const RenderStatus = (props: GridRenderCellParams<string>) => {
  const statusesTag = {
    CURATED: ["Accepted", "success"],
    REJECTED: ["Rejected", "error"],
    QUEUE: ["In Queue", "warning"],
  };

  return (
    <Box
      bgcolor={`${statusesTag[props.value][1]}.contrastText`}
      px={1}
      py={0.25}
      borderRadius="1rem"
    >
      <Typography
        variant="caption"
        align="left"
        color={`${statusesTag[props.value][1]}.main`}
        component="div"
      >
        {statusesTag[props.value][0]}
      </Typography>
    </Box>
  );
};

interface ValueProps {
  row: Antibody;
  field: string;
}

const getValueOrEmpty = (props: ValueProps) => {
  return props.row[props.field] ?? "";
}

const getList = (props: ValueProps) => {
  return props.row[props.field]?.join(", ") ?? "";
};

const getNameAndId = (props: ValueProps) => {
  return `${props.row.abName} AB_${props.row.abId}`
};


const getValueForCitation = (props: ValueProps) => {
  return getProperCitation(props.row);
};

const columnsDefaultProps = {
  flex: 1,
  renderCell: RenderCellContent,
  headerClassName: "custom-header",
};

const dataGridStyles = {
  "&.MuiDataGrid-root": {
    border: "0px",
  },
  "& .MuiDataGrid-main": {
    border: "0.063rem solid",
    borderColor: "grey.200",
    borderTopLeftRadius: "8px",
    borderTopRightRadius: "8px",
    "& div":{
      pointerEvents:'auto'
    },
  },
  "& .MuiDataGrid-row:hover": {
    backgroundColor: "grey.50",
  },
  "& .MuiDataGrid-columnHeadersInner": {
    backgroundColor: "grey.50",
  },
  "& .MuiDataGrid-columnHeaderTitle": {
    color: "grey.500",
    fontWeight: 600,
    fontSize: "0.875rem",
  },
  " .MuiDataGrid-columnSeparator": {
    display: "none",
  },
  "& .custom-header": {
    borderRight: "0.063rem solid",
    borderColor: "grey.200",
  },
  "& .MuiCheckbox-root.MuiCheckbox-indeterminate svg": {
    width: "1.25rem",
    height: "1.25rem",
    backgroundColor: "common.white",
    border: "0.063rem solid",
    borderColor: "grey.300",
    borderRadius: "0.375rem",
  },
  "& .MuiCheckbox-root.MuiCheckbox-indeterminate svg path": {
    display: "none",
  },
  "& .MuiDataGrid-iconButtonContainer": {
    visibility: "visible",
  },
};

const AntibodiesTable = (props) => {
  const user = useContext(UserContext)[0];
  const currentPath = window.location.pathname;
  const [antibodiesList, setAntibodiesList] = useState<Antibody[]>();
  const { activeSearch, searchedAntibodies, loader } = useContext(SearchContext)

  const fetchAntibodies = () => {
    !activeSearch
      ? (
        getAntibodies()
          .then((res) => {
            return setAntibodiesList(res.items);
          })
          .catch((err) => alert(err))
      )
      : setAntibodiesList(searchedAntibodies)
  };

  const fetchUserAntibodies = () => {
    getUserAntibodies()
      .then((res) => {
        return setAntibodiesList(res.items);
      })
      .catch((err) => alert(err));
  };

  useEffect(() => {
    props.activeTab === ALLRESULTS
      ? fetchAntibodies()
      : user && fetchUserAntibodies();
  }, [activeSearch, searchedAntibodies]);


  const columns: GridColDef[] = [
    {
      ...columnsDefaultProps,
      field: "abName",
      headerName: "Name",
      hide: true,
    },
    {
      ...columnsDefaultProps,
      field: "abId",
      headerName: "ID",
      hide: true,
    },
    {
      ...columnsDefaultProps,
      field: "nameAndId",
      headerName: "Name & ID",
      flex: 3,
      renderCell: RenderNameAndId,
      valueGetter: getNameAndId,
      headerAlign: "left",
      align: "left",
    },
    // {
    //   ...columnsDefaultProps,
    //   field: "abTarget",
    //   headerName: "Target antigen (excl. species)",
    //   hide: true,
    // },
    {
      ...columnsDefaultProps,
      field: "targetSpecies",
      headerName: "Target species",
      valueGetter: getList,
      hide: true,
    },
    {
      ...columnsDefaultProps,
      field: "applications",
      headerName: "Applications",
      valueGetter: getList,
      hide: true,
    },
    {
      ...columnsDefaultProps,
      field: "abTarget",
      headerName: "Target antigen",
      flex: 1.5,
      valueGetter: getValueOrEmpty,
    },
    {
      ...columnsDefaultProps,
      field: "properCitation",
      headerName: "Proper citation",
      flex: 2,
      valueGetter: getValueForCitation,
      renderCell: RenderProperCitation,
      type: "actions",
    },
    {
      ...columnsDefaultProps,
      field: "clonality",
      headerName: "Clonality",
    },
    {
      ...columnsDefaultProps,
      field: "reference",
      headerName: "Reference",
      flex: 1.5,
      hide: true,
    },
    {
      ...columnsDefaultProps,
      field: "comments",
      headerName: "Comments",
      renderCell: RenderHtml,
      flex: 3,
      align: "left",
    },
    {
      ...columnsDefaultProps,
      field: "cloneId",
      headerName: "Clone ID",
      hide: true,
    },
    {
      ...columnsDefaultProps,
      field: "sourceOrganism",
      headerName: "Host organism",
      flex: 1.5,
    },
    {
      ...columnsDefaultProps,
      field: "vendorName",
      headerName: "Link to Vendor",
      flex: 1.5,
      type: "actions",
    },
    {
      ...columnsDefaultProps,
      field: "catalogNum",
      headerName: "Cat Num",
    },
    {
      ...columnsDefaultProps,
      field: "url",
      headerName: "Product URL",
      hide: true,
    },
    {
      ...columnsDefaultProps,
      field: "status",
      headerName: "Status",
      hide: props.activeTab === ALLRESULTS,
      renderCell: RenderStatus,
      flex: 1.3,
    },
  ];

  const compProps = {
    toolbar: {
      activeTab: props.activeTab,
    },
    noRowsOverlay:{
      activeSearch: activeSearch
    },
    panel: {
      sx: {
        "& .MuiTypography-body1": {
          fontSize: "0.875rem",
          color: "grey.500",
        },
      },
    },
    filterPanel: {
      filterFormProps: {
        columnInputProps: {
          variant: "outlined",
          size: "small",
          sx: { mr: 1 },
        },
        operatorInputProps: {
          variant: "outlined",
          size: "small",
          sx: { mr: 1 },
        },
        valueInputProps: {
          InputComponentProps: {
            variant: "outlined",
            size: "small",
          },
        },
      },
      sx: {
        "& .MuiDataGrid-filterForm": {
          "& .MuiFormControl-root": {
            "& legend": {
              display: "none",
            },
            "& fieldset": {
              top: 0,
            },
            "& .MuiFormLabel-root": {
              display: "none",
            },
          },
        },
      },
    },
    columnMenu: {
      sx: {
        "& .MuiMenuItem-root": {
          fontSize: "0.875rem",
          color: "grey.500",
        },
      },
    },
  };

  const NoRowsOverlay = () => typeof activeSearch==='string' && activeSearch !== '' && searchedAntibodies.length === 0? <NotFoundMessage activeSearch={activeSearch}/>:typeof activeSearch !== 'string'? <Error500 />: <GridNoRowsOverlay/>

  const SortIcon = ({ sortingOrder, ...other }) => <SortingIcon {...other} />

  return (
    <Box>
      <Box sx={{ flexGrow: 1, height: "90vh" }}>
        {currentPath === "/submissions" && !user ? (
          <ConnectAccount />
        ) :(
          <DataGrid
            sx={dataGridStyles}
            rows={antibodiesList ?? []}
            getRowId={getRowId}
            columns={columns}
            pageSize={10}
            rowsPerPageOptions={[20]}
            checkboxSelection
            disableSelectionOnClick
            getRowHeight={() => "auto"}
            loading={!antibodiesList|| loader}
  
            components={{
              BaseCheckbox: StyledCheckBox,
              ColumnFilteredIcon: FilteredColumnIcon,
              ColumnUnsortedIcon: SortIcon,
              ColumnSortedAscendingIcon: AscSortedIcon,
              ColumnSortedDescendingIcon: DescSortedIcon,
              Toolbar: CustomToolbar,
              ColumnMenuIcon: FilterIcon,
              ColumnSelectorIcon: SettingsIcon,
              NoRowsOverlay: NoRowsOverlay
            }}
            componentsProps={compProps}
            localeText={{
              toolbarColumns: "Table settings",
            }}
          /> 
        )}
      </Box>
    </Box>
  );
};

export default AntibodiesTable;
