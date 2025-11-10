import React, { useEffect, useState, useContext, useCallback, useMemo } from "react";
//MUI
import {
  DataGrid,
  useGridApiContext,
  GridColDef,
  GridRenderCellParams,
  GridCsvExportOptions,
  GridNoRowsOverlay,
  GridColumnVisibilityModel,
  GridFilterModel
} from "@mui/x-data-grid";
import {
  Typography,
  Box,
  Link,
  Checkbox,
  Popover,
  Button
} from "@mui/material";

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
import TableHeader from "./HomeHeader";
import { Antibody } from "../../rest";
import { checkIfFilterSetExists, getColumnsToDisplay, getProperCitation, getRandomId } from "../../utils/antibody";
import { UserContext } from "../../services/UserService";
import ConnectAccount from "./ConnectAccount";
import { ALLRESULTS, SEARCH_MODES, MYSUBMISSIONS, BLANK_FILTER_MODEL } from "../../constants/constants";
import SearchContext, { SearchContextProps } from "../../context/search/SearchContext";
import NotFoundMessage from "./NotFoundMessage";
import Error500 from "../UI/Error500";
import { PAGE_SIZE } from "../../constants/constants";
import { TablePaginatedFooter } from "./TablePaginatedFooter";
import { CustomFilterPanel } from "./CustomFilterPanel";
import { trackVendorClick } from "../../utils/tracking";



const StyledCheckBox = (props) => {
  return (
    <Checkbox
      {...props}
      checkedIcon={<CheckedIcon />}
      icon={<UncheckedIcon />}
    />
  );
};

const getRowId = (ab: Antibody) => `${ab.ix}`;

const SortIcon = ({ ...other }) => <SortingIcon {...other} />;

interface CustomToolbarProps {
  activeTab?: string;
  searchedAntibodies?: Antibody[];
  filterModel?: GridFilterModel;
  [key: string]: any; // Allow additional props from DataGrid
}

const CustomToolbar = (props: CustomToolbarProps) => {
  const { 
    activeTab = ALLRESULTS, 
    searchedAntibodies = [], 
    filterModel = { items: [] } 
  } = props;
  
  const [activeSelection, setActiveSelection] = useState(true);
  const searchContext = useContext(SearchContext);
  const warningMessage = searchContext?.warningMessage;
  const apiRef = useGridApiContext();
  const selectedRows = apiRef.current.getSelectedRows();

  const handleExport = (options: GridCsvExportOptions) =>
    apiRef.current.exportDataAsCsv(options);

  const showFilterMenu = () => apiRef.current.showFilterPanel();

  useEffect(() => {
    if (selectedRows.size === 0) {
      setActiveSelection(false);
    } else {
      setActiveSelection(true);
    }
  }, [selectedRows]);

  return (
    <><TableHeader
      activeSelection={activeSelection}
      handleExport={handleExport}
      showFilterMenu={showFilterMenu}
      activeTab={activeTab}
      filterModel={filterModel}
      warningMessage={warningMessage}
      shownResultsNum={searchedAntibodies.length}
    />

    </>
  );
};

const RenderNameAndId = (props: GridRenderCellParams) => {
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
        sx={{
          color: "grey.700",
          fontWeight: 500
        }}
      >
        {props.row.abName}
      </Typography>
      <Typography
        variant="caption"
        align="left"
        component="div"
        sx={{
          color: "grey.500"
        }}
      >
        AB_{props.row.abId}
      </Typography>
    </Link>
  );
};


const getValueOrEmpty = (_: any, row: Antibody, column: GridColDef) => {
  return row[column.field] ?? "";
};

const RenderCellContent = (props: GridRenderCellParams) => {
  return (
    <Typography
      variant="caption"
      align="left"
      component="div"
      className="col-content"
      sx={{
        color: "grey.500"
      }}
    >
      {props.field === "targetAntigen"
        ? `${props.row.abTarget} ${props.row.targetSpecies.join(", ")}`
        : props.value}
    </Typography>
  );
};

const RenderVendor = (props) => {
  const handleClick = useCallback(() => trackVendorClick(props.row.vendorName, props.row.vendorId), [props.row.vendorName, props.row.vendorId]);
  return <Typography
    variant="caption"
    align="left"
    component="div"
    className="col-vendor"
    onClick={handleClick}
    sx={{
      color: "grey.500",
      width: "fit-content"
    }}
  >
    {props.row.url ? <Link
      className="link-vendor"
      underline="none"
      target="_blank"
      href={props.row.url}
      sx={{
        bgcolor: "primary.light",
        px: 0.5,
        py: 0.25,
        display: "block"
      }}
    >
      {props.value}
    </Link> : props.value}
  </Typography>
}

const RenderClonality = (props) => (
  <Typography
    variant="caption"
    align="left"
    component="div"
    className="col-clonality"
    sx={{
      color: "grey.500",
      bgcolor: "grey.A200",
      px: 1,
      py: 0.25,
      borderRadius: "1rem",
      width: "fit-content"
    }}
  >
    {props.value}
  </Typography>
);


const RenderHtml = (props: GridRenderCellParams<any>) => {
  return (
    <Typography
      variant="caption"
      align="left"
      component="div"
      dangerouslySetInnerHTML={{ __html: props.value }}
      className="col-html"
      sx={{
        color: "grey.500"
      }}
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

const RenderProperCitation = (props: GridRenderCellParams<any>) => {

  const [anchorCitationPopover, setAnchorCitationPopover] =
    useState<HTMLButtonElement | null>(null);

  const handleCloseCitation = useCallback(() => {
    setAnchorCitationPopover(null);
  }, [setAnchorCitationPopover]);

  const handleClickCitation = useCallback(async (event) => {
    const target = event.currentTarget;
    try {
      await navigator.clipboard.writeText(props.value);
      setAnchorCitationPopover(target);
      setTimeout(handleCloseCitation, 1000);
    } catch (err) {
      console.error('Failed to copy citation:', err);
    }
  }, [handleCloseCitation, setAnchorCitationPopover, props.value]);



  const open = Boolean(anchorCitationPopover);

  return props && (
    <Box sx={citationStyles.citationColumn} className="col-proper-citation">
      <Typography
        variant="caption"
        align="left"
        component="div"
        sx={{
          color: props.field === "vendor" ? "primary.main" : "grey.500"
        }}
      >
        {props.value}
      </Typography>
      <Button
        onClick={handleClickCitation}
        size="small"
        sx={{ minWidth: 0 }}
        startIcon={
          <CopyIcon sx={theme => ({
            stroke: theme.palette.grey[500]
          })} fontSize="inherit" />
        }
        className="btn-citation-copy"
      />
      {open && <Popover
        open={open}
        anchorEl={anchorCitationPopover}
        onClose={handleCloseCitation}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "center",
        }}
        transformOrigin={{
          vertical: "top",
          horizontal: "center",
        }}
        disableRestoreFocus
      >
        <Typography className="msg-citation-copied" sx={citationStyles.popover}>Citation copied</Typography>
      </Popover>}
    </Box>
  );
};

const RenderStatus = (props: GridRenderCellParams<any>) => {
  const statusesTag = {
    CURATED: ["Accepted", "success"],
    REJECTED: ["Rejected", "error"],
    QUEUE: ["In Queue", "warning"],
    UNDER_REVIEW: ["Under Review", "warning"],
  };

  return (
    <Box
      className="col-status"
      sx={{
        bgcolor: `${statusesTag[props.value][1]}.contrastText`,
        px: 1,
        py: 0.25,
        borderRadius: "1rem"
      }}
    >
      <Typography
        variant="caption"
        align="left"
        component="div"
        sx={{
          color: `${statusesTag[props.value][1]}.main`
        }}
      >
        {statusesTag[props.value][0]}
      </Typography>
    </Box>
  );
};


const getList = (_: any, row: Antibody, column: GridColDef) => {
  return row[column.field]?.join(", ") ?? "";
};

const getNameAndId = (_: any, row: Antibody) => {
  return `${row.abName} AB_${row.abId}`;
};

const getValueForCitation = (_: any, row: Antibody) => {

  return row ? getProperCitation(row) : "";
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
  "& .MuiDataGrid-row": {
    height: "100%"
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

const AntibodiesTable = (props: any) => {
  const user = useContext(UserContext)?.[0];
  const searchParams = new URLSearchParams(window.location.search);
  const searchQuery = searchParams.get('q');
  const [paginationModel, setPaginationModel] = React.useState({
    pageSize: PAGE_SIZE,
    page: 0,
  });


  const {
    activeSearch,
    searchedAntibodies,
    loader,
    getAntibodyList,
    filterModel,
    setFilterModel,
    sortModel,
    setSortModel,
    totalElements
  } =
    useContext(SearchContext) as SearchContextProps;

  const applyFilterAndSortModels = useCallback((filtermodel, query, sortmodel = sortModel) => {
    // Also does the applyFilterAndSortModels from the CustomFilterPanel - when apply button is clicked
    const searchmode = (props.activeTab === MYSUBMISSIONS) ? SEARCH_MODES.MY_FILTERED_AND_SEARCHED_ANTIBODIES :
      SEARCH_MODES.ALL_FILTERED_AND_SEARCHED_ANTIBODIES
    getAntibodyList(
      searchmode,
      query,
      1,
      filtermodel,
      sortmodel
    )
    if (filtermodel !== filterModel) {
      setFilterModel(filtermodel);
    }
    if (sortmodel !== sortModel) {
      setSortModel(sortmodel);
    }
  }, [filterModel, sortModel, getAntibodyList, props.activeTab, setFilterModel, setSortModel]);

  const addSortingColumn = useCallback((sortmodel) => {
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
  }, [filterModel, searchQuery, activeSearch, getAntibodyList, props.activeTab, setSortModel]);

  const setNewFilterColumn = useCallback((model) => {
    const newblankFilter = { ...BLANK_FILTER_MODEL, columnField: model.items[0].field, field: model.items[0].field, id: getRandomId() }
    filterModel.items.push(newblankFilter);
    setFilterModel(filterModel);
  }, [filterModel, setFilterModel]);
  const addNewFilterColumn = useCallback((model) => {
    if (!checkIfFilterSetExists(model, filterModel)) {
      setNewFilterColumn(model);
    }
  }, [filterModel, setNewFilterColumn]);


  const activeSearchRef = React.useRef(activeSearch);
  activeSearchRef.current = activeSearch;

  const filterModelRef = React.useRef(filterModel);
  filterModelRef.current = filterModel;

  const sortModelRef = React.useRef(sortModel);
  sortModelRef.current = sortModel;

  useEffect(() => {
    const isSearchInMySubmission = (props.activeTab === MYSUBMISSIONS && activeSearchRef.current)
    // NOTE: LOGIC below - if no filters/sortmodel exist or search query exists in my submission - don't proceed, 
    // since this is handled in separate useEffect
    if (filterModelRef.current.items.length > 0 || sortModelRef.current.length > 0 || isSearchInMySubmission) {
      return;
    }

    if (searchQuery || activeSearchRef.current) {
      getAntibodyList(SEARCH_MODES.SEARCHED_ANTIBODIES, searchQuery || activeSearchRef.current);
    } else if (props.activeTab === MYSUBMISSIONS) {
      getAntibodyList(SEARCH_MODES.MY_ANTIBODIES);
    } else {
      getAntibodyList(SEARCH_MODES.ALL_ANTIBODIES);
    }
  }, [props.activeTab, user, searchQuery, getAntibodyList]);

  useEffect(() => {
    // NOTE: LOGIC below - whenever search query changes and filters exist, then 
    // if filters exist in My Submission - apply with empty search
    // if filters exist in All Results - apply with search query
    if (activeSearch && filterModel.items.length > 0) {
      if (props.activeTab === MYSUBMISSIONS) {
        applyFilterAndSortModels(filterModel, '')
      } else {
        applyFilterAndSortModels(filterModel, searchQuery || activeSearch)
      }
    }
  }, [activeSearch, searchQuery, filterModel, props.activeTab, applyFilterAndSortModels]);

  useEffect(() => {
    // NOTE: LOGIC below - whenever tab is changed
    // if filters/sortmodel exist in My Submission - apply with empty search and empty filters/sortmodel
    // if filters/sortmodel exist in All Results - apply with search query but empty filters/sortmodel
    // if no filters/sortmodel exist in My Submission - get My Submissions
    // if no filters/sortmodel exist in All Results - this case is handled in the first useEffect 
    if (filterModel.items.length > 0 || sortModel.length > 0) {
      if (props.activeTab === MYSUBMISSIONS) {
        applyFilterAndSortModels({ items: [] }, '', [])
      } else {
        applyFilterAndSortModels({ items: [] }, searchQuery || activeSearch, [])
      }

    } else {
      if (props.activeTab === MYSUBMISSIONS) {
        getAntibodyList(SEARCH_MODES.MY_ANTIBODIES)
      }

    }

  }, [props.activeTab]);

  const columns: GridColDef[] = useMemo( () => [
    {
      ...columnsDefaultProps,
      field: "abName",
      headerName: "Name",
      hideable: true,
      display: "flex",
    },
    {
      ...columnsDefaultProps,
      field: "abId",
      headerName: "ID",
      hideable: true,
      display: "flex",
    },
    {
      ...columnsDefaultProps,
      field: "accession",
      headerName: "Accession",
      hideable: true,
      display: "flex",
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
      display: "flex",
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
      hideable: true,
      sortable: false,
      display: "flex",
    },
    {
      ...columnsDefaultProps,
      field: "applications",
      headerName: "Applications",
      valueGetter: getList,
      sortable: false,
      hideable: true,
      display: "flex",
    },
    {
      ...columnsDefaultProps,
      field: "abTarget",
      headerName: "Target antigen",
      flex: 1.5,
      valueGetter: getValueOrEmpty,
      display: "flex",
    },
    {
      ...columnsDefaultProps,
      field: "properCitation",
      headerName: "Proper citation",
      flex: 2,
      valueGetter: getValueForCitation,
      renderCell: RenderProperCitation,
      type: "actions",
      hideable: false,
      headerAlign: "left",
      align: "left",
      display: "flex",
    },
    {
      ...columnsDefaultProps,
      field: "clonality",
      headerName: "Clonality",
      renderCell: RenderClonality,
      flex: 1.5,
      display: "flex",
    },
    {
      ...columnsDefaultProps,
      field: "reference",
      headerName: "Reference",
      flex: 1.5,
      hideable: true,
      filterable: false,
      sortable: false,
      display: "flex",
    },
    {
      ...columnsDefaultProps,
      field: "comments",
      headerName: "Comments",
      renderCell: RenderHtml,
      flex: 3,
      align: "left",
      display: "flex",
    },
    {
      ...columnsDefaultProps,
      field: "cloneId",
      headerName: "Clone ID",
      hideable: true,
      display: "flex",
    },
    {
      ...columnsDefaultProps,
      field: "sourceOrganism",
      headerName: "Host organism",
      flex: 1.5,
      display: "flex",
    },
    {
      ...columnsDefaultProps,
      field: "vendorName",
      headerName: "Vendor",
      flex: 1.5,
      renderCell: RenderVendor,
      display: "flex",
    },
    {
      ...columnsDefaultProps,
      field: "catalogNum",
      headerName: "Cat Num",
      display: "flex",
    },
    {
      ...columnsDefaultProps,
      field: "numOfCitation",
      headerName: "Citations",
      flex: 1,
      filterable: false,
      sortable: true,
      align: 'right',
      hideable: false,
      display: "flex",
    },
    {
      ...columnsDefaultProps,
      field: "url",
      headerName: "Product URL",
      hideable: true,
      sortable: false,
      filterable: false,
      display: "flex",
    },
    {
      ...columnsDefaultProps,
      field: "status",
      headerName: "Status",
      hideable: props.activeTab === ALLRESULTS,
      renderCell: RenderStatus,
      flex: 1.4,
      filterable: false,
      sortable: false,
      display: "flex",
    },
  ], [props.activeTab]);

  const compProps = useMemo(() => ({
    toolbar: {
      activeTab: props.activeTab,
      searchedAntibodies,
      filterModel
    },
    noRows: {
      activeSearch: activeSearch,
    },
    panel: {
      sx: {
        "& .MuiTypography-body1": {
          fontSize: "0.875rem",
          color: "grey.500",
        }
      },
    },
    columnMenu: {
      style: {
        fontSize: "0.875rem",
        color: "grey.500",
      }
    },
    basePopper: {
      sx: {
        "& .MuiListItemText-root .MuiListItemText-primary": {
          display: "flex"
        }
      }
    }
  }), [props.activeTab, searchedAntibodies, filterModel, activeSearch]);

  const [showColumns, setShowColumns] = useState<GridColumnVisibilityModel>(getColumnsToDisplay(columns));

  const NoRowsOverlay = () =>
    typeof activeSearch === "string" &&
      activeSearch !== "" &&
      searchedAntibodies?.length === 0 ? (
        <NotFoundMessage activeSearch={activeSearch} />
      ) : typeof activeSearch !== "string" ? (
        <Error500 />
      ) : (
        <GridNoRowsOverlay />
      );

  
  const currentPath = window.location.pathname;
  return (
    <Box>

      <Box sx={{ flexGrow: 1, height: "83.5vh" }}>

        {currentPath === "/submissions" && !user ? (
          <ConnectAccount />
        ) : (
          <DataGrid
            className="antibodies-table"
            filterModel={filterModel}
            sx={dataGridStyles}
            rows={searchedAntibodies ?? []}
            getRowId={getRowId}
            columns={columns}
            paginationModel={paginationModel}
            onPaginationModelChange={setPaginationModel}
            pageSizeOptions={[20]}
            pagination={true}
            paginationMode="server"
            rowCount={totalElements}
            sortingMode="server"
            sortModel={sortModel}
            onSortModelChange={addSortingColumn}
            checkboxSelection
            disableRowSelectionOnClick
            columnVisibilityModel={showColumns || {}}
            onColumnVisibilityModelChange={setShowColumns}
            getRowHeight={() => "auto"}
            loading={!searchedAntibodies || loader}
            onFilterModelChange={addNewFilterColumn}
            filterMode="server"
            slots={{
              baseCheckbox: StyledCheckBox,
              columnFilteredIcon: FilteredColumnIcon,
              columnUnsortedIcon: SortIcon,
              columnSortedAscendingIcon: AscSortedIcon,
              columnSortedDescendingIcon: DescSortedIcon,
              toolbar: CustomToolbar,
              columnMenuIcon: MoreVertIcon,
              columnSelectorIcon: SettingsIcon,
              noRowsOverlay: NoRowsOverlay,
              footer: TablePaginatedFooter,
              filterPanel: () => CustomFilterPanel({
                columns,
                filterModel,
                applyFilterAndSortModels,
                setFilterModel,
              }),
            }}
            slotProps={compProps}
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




