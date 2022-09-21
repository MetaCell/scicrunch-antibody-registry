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
import { Antibody } from "../../rest";

const StyledBadge = (props) => {
  if (props.field === "vendor") {
    return (
      <Box bgcolor="primary.light" px={0.5} py={0.25} borderRadius="0.25rem">
        <Link
          underline="none"
          target="_blank"
          href={`https://${props.row.url}`}
        >
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

const getRowId = (ab: Antibody) => ab.abId;

const CustomToolbar = () => {
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
        {props.field === "targetAntigen"
          ? `${props.row.abTarget} ${props.row.targetSpecies}`
          : props.value}
      </Typography>
    </StyledBadge>
  );
};

const RenderProperCitation = (props: GridRenderCellParams<String>) => {
  return <StyledBadge {...props}>
    <Typography
      variant="caption"
      align="left"
      color={props.field === "vendor" ? "primary.main" : "grey.500"}
      component="div"
    >
     ({props.row.vendorName}#{props.row.catalogNum}, RRID:AB_{props.row.abId})
    </Typography>
  </StyledBadge>
}

interface ValueProps {
  row: Antibody;
  field: string;
}


const getValueOrEmpty = (props: ValueProps) => {
  return props.row[props.field] ?? "";
}

const getValueProperCitation = (props: ValueProps) => {
  return "";
}


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
  "& .MuiDataGrid-cell": {
    cursor: "pointer",
  },
};
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
    flex: 2,
    renderCell: RenderNameAndId,
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
    valueGetter: getValueProperCitation,
    renderCell: RenderProperCitation
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
    field: "cloneId",
    headerName: "Clone ID",
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
];

const AntibodiesTable = () => {
  const [antibodiesList, setAntibodiesList] = useState([]);

  const fetchAntibodies = () => {
    getAntibodies()
      .then((res) => {
        return setAntibodiesList(res.items);
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
          getRowId={getRowId}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[20]}
          checkboxSelection
          disableSelectionOnClick
          getRowHeight={() => "auto"}
          onRowClick={(params) =>
            (window.location.href = `/${params.row.abId}`)
          }
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
