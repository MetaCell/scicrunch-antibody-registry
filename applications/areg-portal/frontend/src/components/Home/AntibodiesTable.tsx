import React, { useEffect, useState } from "react";
//MUI
import {
  DataGrid,
  useGridApiContext,
  GridColDef,
  GridRenderCellParams,
  GridCsvExportOptions,
} from "@mui/x-data-grid";
import { Typography, Box, Link, Checkbox } from "@mui/material";

//project imports
import { getAntibodies } from "../../services/AntibodiesService";
import {
  AscSortedIcon,
  DescSortedIcon,
  FilteredColumnIcon,
  SortingIcon,
  CheckedIcon,
  UncheckedIcon,
  FilterIcon,
  SettingsIcon,
} from "../icons";
import HomeHeader from "./HomeHeader";

const StyledBadge = (props) => {
  if (props.field === "vendor") {
    return (
      <Box bgcolor="primary.light" px={0.5} py={0.25} borderRadius="0.25rem">
        <Link component="button" underline="none">
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

const CustomToolbar = ({ setPanelAnchorEl }) => {
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
      setPanelAnchorEl={setPanelAnchorEl}
    />
  );
};

const RenderNameAndId = (props: GridRenderCellParams<String>) => {
  return (
    <Box>
      <Typography
        variant="body2"
        align="left"
        color="grey.700"
        fontWeight={500}
      >
        {props.row.ab_name}
      </Typography>
      <Typography
        variant="caption"
        align="left"
        component="div"
        color="grey.500"
      >
        {props.row.ab_id}
      </Typography>
    </Box>
  );
};

const RenderCellContent = (props: GridRenderCellParams<String>) => {
  return (
    <StyledBadge {...props}>
      <Typography
        variant="caption"
        align="left"
        color={props.field === "vendor" ? "primary.main" : "grey.500"}
        component="div"
      >
        {props.field === "target_ant_spec"
          ? `${props.row.ab_target} ${props.row.target_species}`
          : props.value}
      </Typography>
    </StyledBadge>
  );
};

const getValue = (props) => {
  let cellValue = "";
  props.field === "ab_name_id"
    ? (cellValue = `${props.row.ab_name || ""} ${props.row.ab_id || ""}`)
    : (cellValue = `${props.row.ab_target || ""} ${
        props.row.target_species || ""
      }`);
  return cellValue;
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
const columns: GridColDef[] = [
  {
    ...columnsDefaultProps,
    field: "ab_name",
    headerName: "Name",
    hide: true,
  },
  {
    ...columnsDefaultProps,
    field: "ab_id",
    headerName: "ID",
    hide: true,
  },
  {
    ...columnsDefaultProps,
    field: "ab_name_id",
    headerName: "Name & ID",
    flex: 2,
    renderCell: RenderNameAndId,
    valueGetter: getValue,
    headerAlign: "left",
    align: "left",
  },
  {
    ...columnsDefaultProps,
    field: "ab_target",
    headerName: "Target antigen (excl. species)",
    hide: true,
  },
  {
    ...columnsDefaultProps,
    field: "target_species",
    headerName: "Target species",
    hide: true,
  },
  {
    ...columnsDefaultProps,
    field: "target_ant_spec",
    headerName: "Target antigen",
    flex: 1.5,
    valueGetter: getValue,
  },
  {
    ...columnsDefaultProps,
    field: "proper_citation",
    headerName: "Proper citation",
    flex: 2,
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
  },
  {
    ...columnsDefaultProps,
    field: "comments",
    headerName: "Comments",
    flex: 3,
    align: "left",
  },
  {
    ...columnsDefaultProps,
    field: "clone_id",
    headerName: "Clone ID",
  },
  {
    ...columnsDefaultProps,
    field: "host",
    headerName: "Host organism",
    flex: 1.5,
  },
  {
    ...columnsDefaultProps,
    field: "vendor",
    headerName: "Link to Vendor",
    flex: 1.5,
  },
  {
    ...columnsDefaultProps,
    field: "catalog_num",
    headerName: "Cat Num",
  },
];

const AntibodiesTable = () => {
  const [antibodiesList, setAntibodiesList] = useState([]);
  // const [panelAnchorEl, setPanelAnchorEl] = React.useState(null);

  const fetchAntibodies = () => {
    getAntibodies()
      .then((res) => {
        return setAntibodiesList(res);
      })
      .catch((err) => alert(err));
  };

  useEffect(fetchAntibodies, []);

  const compProps = {
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

  return (
    <Box>
      <Box sx={{ flexGrow: 1, height: "90vh" }}>
        <DataGrid
          sx={dataGridStyles}
          rows={antibodiesList}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[20]}
          checkboxSelection
          disableSelectionOnClick
          getRowHeight={() => "auto"}
          components={{
            BaseCheckbox: StyledCheckBox,
            ColumnFilteredIcon: FilteredColumnIcon,
            ColumnUnsortedIcon: SortingIcon,
            ColumnSortedAscendingIcon: AscSortedIcon,
            ColumnSortedDescendingIcon: DescSortedIcon,
            Toolbar: CustomToolbar,
            ColumnMenuIcon: FilterIcon,
            ColumnSelectorIcon: SettingsIcon,
          }}
          componentsProps={compProps}
          localeText={{
            toolbarColumns: "Table settings",
          }}
        />
      </Box>
    </Box>
  );
};

export default AntibodiesTable;
