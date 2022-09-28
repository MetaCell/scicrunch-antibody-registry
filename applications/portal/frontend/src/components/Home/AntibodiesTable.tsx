import React, { useEffect, useState } from "react";
//MUI
import {
  DataGrid,
  useGridApiContext,
  GridColDef,
  GridRenderCellParams,
  GridCsvExportOptions,
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
  CopyIcon,
} from "../icons";
import HomeHeader from "./HomeHeader";
import { Antibody } from "../../rest";
import { getProperCitation } from "../../utils/antibody";
import { useTheme } from "@mui/system";
import { useUser, User } from "../../services/UserService";
import ConnectAccount from "./ConnectAccount";

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

const getRowId = (ab: Antibody) => ab.abId;

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
        color={props.field === "vendorName" ? "primary.main" : "grey.500"}
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

interface ValueProps {
  row: Antibody;
  field: string;
}

const getValueOrEmpty = (props: ValueProps) => {
  return props.row[props.field] ?? "";
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

const AntibodiesTable = (props) => {
  const user: User = useUser();
  const currentPath = window.location.pathname;
  const [antibodiesList, setAntibodiesList] = useState([]);

  const fetchAntibodies = () => {
    getAntibodies()
      .then((res) => {
        return setAntibodiesList(res.items);
      })
      .catch((err) => alert(err));
  };

  const fetchUserAntibodies = () => {
    const items = [
      {
        clonality: "unknown",
        epitope: null,
        comments: null,
        url: "https://www.cellsignal.com/products/antibody-conjugates/neun-d4g4o-xp-rabbit-mab-alexa-fluor-488-conjugate/54761",
        abName: "hh",
        abTarget: "hh",
        catalogNum: "54761",
        cloneId: null,
        commercialType: "personal",
        definingCitation: null,
        productConjugate: null,
        productForm: null,
        productIsotype: null,
        sourceOrganism: null,
        targetSpecies: null,
        uniprotId: null,
        vendorName: "string",
        applications: null,
        kitContents: null,
        accession: "",
        status: "QUEUE",
        feedback: null,
        abId: "25520410",
        catAlt: null,
        curateTime: "2022-09-27T10:02:28.416438+00:00",
        curatorComment: null,
        discDate: null,
        insertTime: "2022-09-27T10:02:28.405856+00:00",
        targetModification: null,
        targetSubregion: null,
        vendorId: 1,
      },
      {
        clonality: "unknown",
        epitope: null,
        comments: null,
        url: "https://www.cellsignal.com/products/antibody-conjugates/neun-d4g4o-xp-rabbit-mab-alexa-fluor-488-conjugate/54761",
        abName: "fgfg",
        abTarget: "ff",
        catalogNum: "54761",
        cloneId: null,
        commercialType: "other",
        definingCitation: null,
        productConjugate: null,
        productForm: null,
        productIsotype: null,
        sourceOrganism: null,
        targetSpecies: null,
        uniprotId: null,
        vendorName: "string",
        applications: null,
        kitContents: null,
        accession: "",
        status: "QUEUE",
        feedback: null,
        abId: "59898603",
        catAlt: null,
        curateTime: "2022-09-27T10:04:11.111390+00:00",
        curatorComment: null,
        discDate: null,
        insertTime: "2022-09-27T10:04:11.100735+00:00",
        targetModification: null,
        targetSubregion: null,
        vendorId: 1,
      },
      {
        clonality: "unknown",
        epitope: null,
        comments: null,
        url: "https://www.cellsignal.com/products/antibody-conjugates/neun-d4g4o-xp-rabbit-mab-alexa-fluor-488-conjugate/54761",
        abName: null,
        abTarget: null,
        catalogNum: "54761",
        cloneId: null,
        commercialType: "commercial",
        definingCitation: null,
        productConjugate: null,
        productForm: null,
        productIsotype: null,
        sourceOrganism: null,
        targetSpecies: null,
        uniprotId: null,
        vendorName: "string",
        applications: null,
        kitContents: null,
        accession: "",
        status: "QUEUE",
        feedback: null,
        abId: "93629159",
        catAlt: null,
        curateTime: "2022-09-27T10:25:23.112356+00:00",
        curatorComment: null,
        discDate: null,
        insertTime: "2022-09-27T10:25:23.049990+00:00",
        targetModification: null,
        targetSubregion: null,
        vendorId: 1,
      },
      {
        clonality: "unknown",
        epitope: null,
        comments: null,
        url: "https://www.cellsignal.com/products/antibody-conjugates/neun-d4g4o-xp-rabbit-mab-alexa-fluor-488-conjugate/54761",
        abName: null,
        abTarget: null,
        catalogNum: "54761",
        cloneId: null,
        commercialType: "commercial",
        definingCitation: null,
        productConjugate: null,
        productForm: null,
        productIsotype: null,
        sourceOrganism: null,
        targetSpecies: null,
        uniprotId: null,
        vendorName: "string",
        applications: null,
        kitContents: null,
        accession: "",
        status: "QUEUE",
        feedback: null,
        abId: "40793895",
        catAlt: null,
        curateTime: "2022-09-27T10:26:12.819677+00:00",
        curatorComment: null,
        discDate: null,
        insertTime: "2022-09-27T10:26:12.811027+00:00",
        targetModification: null,
        targetSubregion: null,
        vendorId: 1,
      },
      {
        clonality: "unknown",
        epitope: null,
        comments: null,
        url: "https://www.cellsignal.com/products/antibody-conjugates/neun-d4g4o-xp-rabbit-mab-alexa-fluor-488-conjugate/54768",
        abName: null,
        abTarget: null,
        catalogNum: "54768",
        cloneId: null,
        commercialType: "commercial",
        definingCitation: null,
        productConjugate: null,
        productForm: null,
        productIsotype: null,
        sourceOrganism: null,
        targetSpecies: null,
        uniprotId: null,
        vendorName: "string",
        applications: null,
        kitContents: null,
        accession: "",
        status: "QUEUE",
        feedback: null,
        abId: "42040869",
        catAlt: null,
        curateTime: "2022-09-27T10:50:52.281340+00:00",
        curatorComment: null,
        discDate: null,
        insertTime: "2022-09-27T10:50:52.270576+00:00",
        targetModification: null,
        targetSubregion: null,
        vendorId: 1,
      },
      {
        clonality: "unknown",
        epitope: null,
        comments: null,
        url: "https://www.cellsignal.com/products/antibody-conjugates/neun-d4g4o-xp-rabbit-mab-alexa-fluor-488-conjugate/54768",
        abName: null,
        abTarget: null,
        catalogNum: "54768",
        cloneId: null,
        commercialType: "commercial",
        definingCitation: null,
        productConjugate: null,
        productForm: null,
        productIsotype: null,
        sourceOrganism: null,
        targetSpecies: null,
        uniprotId: null,
        vendorName: "string",
        applications: null,
        kitContents: null,
        accession: "",
        status: "QUEUE",
        feedback: null,
        abId: "53695027",
        catAlt: null,
        curateTime: "2022-09-27T10:51:29.605908+00:00",
        curatorComment: null,
        discDate: null,
        insertTime: "2022-09-27T10:51:29.598045+00:00",
        targetModification: null,
        targetSubregion: null,
        vendorId: 1,
      },
      {
        clonality: "unknown",
        epitope: null,
        comments: null,
        url: "https://www.zenhub.com/",
        abName: null,
        abTarget: null,
        catalogNum: "555",
        cloneId: null,
        commercialType: "commercial",
        definingCitation: null,
        productConjugate: null,
        productForm: null,
        productIsotype: null,
        sourceOrganism: null,
        targetSpecies: null,
        uniprotId: null,
        vendorName: "Bio",
        applications: null,
        kitContents: null,
        accession: "",
        status: "QUEUE",
        feedback: null,
        abId: "10283594",
        catAlt: null,
        curateTime: "2022-09-27T10:52:20.865109+00:00",
        curatorComment: null,
        discDate: null,
        insertTime: "2022-09-27T10:52:20.855770+00:00",
        targetModification: null,
        targetSubregion: null,
        vendorId: 2,
      },
    ];
    return setAntibodiesList(items);
  };

  useEffect(() => {
    props.activeTab === "all results"
      ? fetchAntibodies()
      : user && fetchUserAntibodies();
  }, []);

  const compProps = {
    toolbar: {
      activeTab: props.activeTab,
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

  return (
    <Box>
      <Box sx={{ flexGrow: 1, height: "90vh" }}>
        {currentPath === "/submissions" && !user ? (
          <ConnectAccount />
        ) : (
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
              (window.location.href = `/AB_${params.row.abId}`)
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
        )}
      </Box>
    </Box>
  );
};

export default AntibodiesTable;
