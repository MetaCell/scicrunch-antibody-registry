import React, { useEffect, useState } from "react";
//MUI
import {
  DataGrid,
  useGridApiContext,
  GridColDef,
  GridRenderCellParams,
  GridCsvExportOptions,
  GridFilterPanel,
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
  } else return <Box>{props.children}</Box>;
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

const CustomToolbar = ({ setFilterButtonEl }) => {
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
      setFilterButtonEl={setFilterButtonEl}
    />
  );
};

// const CustomFilterPanel = React.forwardRef<
//   HTMLUListElement,
//   GridColumnMenuProps
// >(function GridColumnMenu(props: GridColumnMenuProps, ref) {
//   const { hideMenu, currentColumn } = props;
//   const apiRef = useGridApiContext();

//   const getDefaultItem = React.useCallback((): GridFilterItem | null => {
//     return {
//       columnField: currentColumn.field,
//       //chequear esto
//       operatorValue: currentColumn.filterOperators![0].value,
//       id: Math.round(Math.random() * 1e5),
//     };
//   }, []);

//   const item = getDefaultItem();

//   const applyFilter = React.useCallback(
//     (item: GridFilterItem) => {
//       apiRef.current.upsertFilterItem(item);
//     },
//     [apiRef]
//   );

//   const deleteFilter = React.useCallback(
//     (item: GridFilterItem) => {
//       const shouldCloseFilterPanel = true;
//       apiRef.current.deleteFilterItem(item);
//       if (shouldCloseFilterPanel) {
//         apiRef.current.hideFilterPanel();
//       }
//     },
//     [apiRef]
//   );

//   const applyFilterLinkOperator = React.useCallback(
//     (operator: GridLinkOperator) => {
//       apiRef.current.setFilterLinkOperator(operator);
//     },
//     [apiRef]
//   );

//   return (
//     <>
//       <GridFilterForm
//         item={item}
//         deleteFilter={deleteFilter}
//         hasMultipleFilters={false}
//         applyMultiFilterOperatorChanges={applyFilterLinkOperator}
//         applyFilterChanges={applyFilter}
//       />
//     </>
//   );
// });

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
    headerName: "Target antigen",
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
  const [filterButtonEl, setFilterButtonEl] = React.useState(null);

  const fetchAntibodies = () => {
    getAntibodies()
      .then((res) => {
        return setAntibodiesList(res);
      })
      .catch((err) => alert(err));
  };

  useEffect(fetchAntibodies, []);

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
          //disableColumnMenu
          disableSelectionOnClick
          getRowHeight={() => "auto"}
          components={{
            BaseCheckbox: StyledCheckBox,
            ColumnFilteredIcon: FilteredColumnIcon,
            ColumnUnsortedIcon: SortingIcon,
            ColumnSortedAscendingIcon: AscSortedIcon,
            ColumnSortedDescendingIcon: DescSortedIcon,
            Toolbar: CustomToolbar,
            ColumnMenu: GridFilterPanel,
            ColumnMenuIcon: FilterIcon,
          }}
          componentsProps={{
            panel: {
              anchorEl: filterButtonEl,
              placement: "bottom-end",
            },
            toolbar: { setFilterButtonEl: setFilterButtonEl },
          }}
        />
      </Box>
    </Box>
  );
};

export default AntibodiesTable;
