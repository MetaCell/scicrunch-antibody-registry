import React, { useEffect, useState, useContext, useCallback } from "react";
//MUI
import {
  DataGrid,
  useGridApiContext,
  GridColDef,
  GridRenderCellParams,
  GridCsvExportOptions,
  GridNoRowsOverlay
} from "@mui/x-data-grid";
import {
  Typography,
  Box,
  Link,
  Checkbox,
  Popover,
  Button
} from "@mui/material";
import { CopyToClipboard } from "react-copy-to-clipboard";

//project imports
import {
  AscSortedIcon,
  DescSortedIcon,
  FilteredColumnIcon,
  SortingIcon,
  CheckedIcon,
  UncheckedIcon,
  SettingsIcon,
  CopyIcon,
} from "../icons";
import MoreVertIcon from '@mui/icons-material/MoreVert';
import HomeHeader from "./HomeHeader";
import { Antibody } from "../../rest";
import { checkIfFilterSetExists, getProperCitation, getRandomId } from "../../utils/antibody";
import { UserContext } from "../../services/UserService";
import ConnectAccount from "./ConnectAccount";
import { ALLRESULTS, SEARCH_MODES, MYSUBMISSIONS, BLANK_FILTER_MODEL } from "../../constants/constants";
import SearchContext from "../../context/search/SearchContext";
import NotFoundMessage from "./NotFoundMessage";
import Error500 from "../UI/Error500";
import { PAGE_SIZE } from "../../constants/constants";
import { TablePaginatedFooter } from "./TablePaginatedFooter";
import { CustomFilterPanel } from "./CustomFilterPanel";


const StyledCheckBox = (props) => {
  return (
    <Checkbox
      {...props}
      checkedIcon={<CheckedIcon />}
      icon={<UncheckedIcon />}
    />
  );
};

const getRowId = (ab: Antibody) => `${ab.abId}${Math.random()}`;

const CustomToolbar = ({ activeTab, searchedAntibodies }) => {
  const [activeSelection, setActiveSelection] = useState(true);
  const {
    warningMessage
  } = useContext(SearchContext);
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
    <><HomeHeader
      activeSelection={activeSelection}
      handleExport={handleExport}
      showFilterMenu={showFilterMenu}
      activeTab={activeTab}
      warningMessage={warningMessage}
      shownResultsNum={searchedAntibodies?.length}
    />
    
    </>
  );
};

const RenderNameAndId = (props: GridRenderCellParams<String>) => {
  const currentPath = window.location.pathname;
  const href =
    currentPath === "/submissions"
      ? `/update/${props.row.accession}`
      : `/AB_${props.row.abId}`;
  return (
    <Link href={href} className="col-name-id">
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
  const cellMapper = {
    ab_target: (row) => `${row.abTarget} ${row.targetSpecies.join(", ")}`,
    ab_name: (row) => row.abName,
    ab_id: (row) => row.abId,
    species: (row) => `${row.targetSpecies.join(", ")}`,
    clone_id: (row) => row.cloneId,
    source_organism: (row) => row.sourceOrganism,
    catalog_num: (row) => row.catalogNum,
  };
  return (
    <Typography
      variant="caption"
      align="left"
      color={"grey.500"}
      component="div"
      className="col-content"
    >
      {cellMapper[props.field](props.row)}
    </Typography>
  );
};

const RenderVendor = (props) => ( 
  
  <Typography
    variant="caption"
    align="left"
    color={"grey.500"}
    component="div"
    className="col-vendor"
  >
    {props.row.url ? <Link className="link-vendor" bgcolor="primary.light" px={0.5} py={0.25} display="block" underline="none" target="_blank" href={props.row.url}>
      {props.row.vendorName}
    </Link> : props.row.vendorName}
  </Typography>
)

const RenderClonality = (props) => (
  <Typography
    variant="caption"
    align="left"
    color={"grey.500"}
    bgcolor="grey.A200"
    component="div"
    px={1} py={0.25} borderRadius="1rem"
    className="col-clonality"
  >
    {props.value}
  </Typography>
);


const RenderHtml = (props: GridRenderCellParams<String>) => {
  return (
    <Typography
      variant="caption"
      align="left"
      color="grey.500"
      component="div"
      dangerouslySetInnerHTML={{ __html: props.value }}
      className="col-html"
    />
  );
};


const citationStyles = {
  popover: (theme) => ({
    p: 1,
    backgroundColor: theme.palette.grey[900],
    color: theme.palette.common.white,
    fontSize: "1rem",
  }),

  citationColumn: {
    cursor: "auto",
    display: "flex",
    alignItems: "center",
  },
};

const RenderProperCitation = (props: GridRenderCellParams<String>) => {

  const [anchorCitationPopover, setAnchorCitationPopover] =
    useState<HTMLButtonElement | null>(null);

  const handleCloseCitation = useCallback(() => {
    setAnchorCitationPopover(null);
  }, [setAnchorCitationPopover]);
    
  const handleClickCitation = useCallback((event) => {
    setAnchorCitationPopover(event.currentTarget);
    setTimeout(handleCloseCitation, 1000);
  }, [handleCloseCitation, setAnchorCitationPopover]);

  

  const open = Boolean(anchorCitationPopover);

  return props && (
    <Box sx={citationStyles.citationColumn} className="col-proper-citation">
      <Typography
        variant="caption"
        align="left"
        color={props.field === "vendor" ? "primary.main" : "grey.500"}
        component="div"
      >
        {props.value}
      </Typography>
      <CopyToClipboard text={props.value} >
        <Button
          onClick={handleClickCitation}
          size="small"
          sx={{ minWidth: 0 }}
          startIcon={
            <CopyIcon sx={{ stroke: theme => theme.palette.grey[500] }} fontSize="inherit" />
          }
          className="btn-citation-copy"
        />
      </CopyToClipboard>
      {open && <Popover
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
        <Typography className="msg-citation-copied" sx={citationStyles.popover}>Citation copied</Typography>
      </Popover>}
    </Box>
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
      className="col-status"
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
};

const getList = (props: ValueProps) => {
  return props.row[props.field]?.join(", ") ?? "";
};

const getNameAndId = (props: ValueProps) => {
  return `${props.row.abName} AB_${props.row.abId}`;
};

const getValueForCitation = (props: ValueProps) => {

  return props?.row ? getProperCitation(props.row) : "";
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
    "& div": {
      pointerEvents: "auto",
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
  const searchParams = new URLSearchParams(window.location.search);
  const searchQuery = searchParams.get('q');

  const {
    activeSearch,
    searchedAntibodies,
    loader,
    getAntibodyList,
    filterModel,
    setFilterModel,
    setSortModel,
  } =
    useContext(SearchContext);

  const handleSetFilterAPI = (filtermodel) => {
    const searchmode = (props.activeTab === MYSUBMISSIONS) ? SEARCH_MODES.MY_FILTERED_AND_SEARCHED_ANTIBODIES :
      SEARCH_MODES.ALL_FILTERED_AND_SEARCHED_ANTIBODIES
    getAntibodyList(
      searchmode,
      searchQuery || activeSearch,
      1,
      filtermodel
    )
    filtermodel !== filterModel ? setFilterModel(filtermodel) : null;
  }

  const addSortingColumn = (sortmodel) => {
    const searchmode = (props.activeTab === MYSUBMISSIONS) ? SEARCH_MODES.MY_FILTERED_AND_SEARCHED_ANTIBODIES :
      SEARCH_MODES.ALL_FILTERED_AND_SEARCHED_ANTIBODIES
    getAntibodyList(
      searchmode,
      searchQuery || activeSearch,
      1,
      filterModel,
      sortmodel
    )
    setSortModel(sortmodel)
  }

  const setNewFilterColumn = (model) => {
    let newblankFilter = { ...BLANK_FILTER_MODEL, columnField: model.items[0].columnField, id: getRandomId() }
    filterModel.items.push(newblankFilter);
    setFilterModel(filterModel);
  }
  const addNewFilterColumn = (model) => {
    if (!checkIfFilterSetExists(model, filterModel)) {
      setNewFilterColumn(model);
    }
  }

  useEffect(() => {
    if (filterModel.items.length > 0) {
      return;
    }
    if (searchQuery) {
      getAntibodyList(SEARCH_MODES.SEARCHED_ANTIBODIES, searchQuery);
    } else if (props.activeTab === MYSUBMISSIONS) {
      getAntibodyList(SEARCH_MODES.MY_ANTIBODIES);
    } else {
      getAntibodyList(SEARCH_MODES.ALL_ANTIBODIES);
    }
  }, [props.activeTab, user, searchQuery]);

  useEffect(() => {
    if (activeSearch && filterModel.items.length > 0) {
      handleSetFilterAPI(filterModel);
    }
  }, [activeSearch]);

  useEffect(() => {
    if (filterModel.items.length > 0) {
      handleSetFilterAPI(filterModel);
    }
  }, [props.activeTab]);

  const columns: GridColDef[] = [
    {
      ...columnsDefaultProps,
      field: "ab_name",
      headerName: "Name",
      hide: true,
      renderCell: RenderCellContent,
    },
    {
      ...columnsDefaultProps,
      field: "ab_id",
      headerName: "ID",
      hide: true,
      renderCell: RenderCellContent,
    },
    {
      ...columnsDefaultProps,
      field: "accession",
      headerName: "Accession",
      hide: true,
    },
    {
      ...columnsDefaultProps,
      field: "nameAndId",
      headerName: "Name & ID",
      flex: 3,
      type: "actions",
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
      field: "species",
      headerName: "Target species",
      valueGetter: getList,
      hide: true,
      renderCell: RenderCellContent,
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
      field: "ab_target",
      headerName: "Target antigen",
      flex: 1.5,
      valueGetter: getValueOrEmpty,
    },
    {
      ...columnsDefaultProps,
      field: "defining_citation",
      headerName: "Proper citation",
      flex: 2,
      valueGetter: getValueForCitation,
      renderCell: RenderProperCitation,
      type: "actions",
      hideable: false
    },
    {
      ...columnsDefaultProps,
      field: "clonality",
      headerName: "Clonality",
      renderCell: RenderClonality,
    },
    {
      ...columnsDefaultProps,
      field: "reference",
      headerName: "Reference",
      flex: 1.5,
      hide: true,
      filterable: false,
      sortable: false,
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
      field: "clone_id",
      headerName: "Clone ID",
      hide: true,
      renderCell: RenderCellContent,
    },
    {
      ...columnsDefaultProps,
      field: "source_organism",
      headerName: "Host organism",
      flex: 1.5,
      renderCell: RenderCellContent,
    },
    {
      ...columnsDefaultProps,
      field: "vendor",
      headerName: "Vendor",
      flex: 1.5,
      renderCell: RenderVendor,

    },
    {
      ...columnsDefaultProps,
      field: "catalog_num",
      headerName: "Cat Num",
      renderCell: RenderVendor,
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
      filterable: false,
      sortable: false,
    },
  ];

  const compProps = {
    toolbar: {
      activeTab: props.activeTab,
      searchedAntibodies
    },
    noRowsOverlay: {
      activeSearch: activeSearch,
    },
    panel: {
      sx: {
        "& .MuiTypography-body1": {
          fontSize: "0.875rem",
          color: "grey.500",
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

  const NoRowsOverlay = () =>
    typeof activeSearch === "string" &&
    activeSearch !== "" &&
    searchedAntibodies.length === 0 ? (
        <NotFoundMessage activeSearch={activeSearch} />
      ) : typeof activeSearch !== "string" ? (
        <Error500 />
      ) : (
        <GridNoRowsOverlay />
      );

  const SortIcon = ({ sortingOrder, ...other }) => <SortingIcon {...other} />;
  const currentPath = window.location.pathname;
  return (
    <Box>
      
      <Box sx={{ flexGrow: 1, height: "90vh" }}>
        
        {currentPath === "/submissions" && !user ? (
          <ConnectAccount />
        ) : (
          <DataGrid
            className="antibodies-table"
            sx={dataGridStyles}
            rows={searchedAntibodies ?? []}
            getRowId={getRowId}
            columns={columns}
            pageSize={PAGE_SIZE}
            rowsPerPageOptions={[20]}
            pagination={true}
            paginationMode="server"
            sortingMode="server"
            onSortModelChange={(model) => addSortingColumn(model)}
            checkboxSelection
            disableSelectionOnClick
            getRowHeight={() => "auto"}
            loading={!searchedAntibodies || loader}
            onFilterModelChange={(model) => addNewFilterColumn(model)}
            filterMode="server"
            components={{
              BaseCheckbox: StyledCheckBox,
              ColumnFilteredIcon: FilteredColumnIcon,
              ColumnUnsortedIcon: SortIcon,
              ColumnSortedAscendingIcon: AscSortedIcon,
              ColumnSortedDescendingIcon: DescSortedIcon,
              Toolbar: CustomToolbar,
              ColumnMenuIcon: MoreVertIcon,
              ColumnSelectorIcon: SettingsIcon,
              NoRowsOverlay: NoRowsOverlay,
              Footer: TablePaginatedFooter,
              FilterPanel: () => CustomFilterPanel({
                columns,
                filterModel,
                handleSetFilterAPI,
                setFilterModel,
              }),
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



