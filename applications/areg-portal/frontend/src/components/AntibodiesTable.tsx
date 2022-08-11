import React, { useEffect, useState } from "react";
//MUI
import {
  DataGrid,
  GridToolbar,
  GridColDef,
  GridRenderCellParams,
  GridAlignment,
} from "@mui/x-data-grid";
import { Typography, Box } from "@mui/material";

//project imports
import { getAntibodies } from "../services/AntibodiesService";

const RenderNameAndId = (props: GridRenderCellParams<String>) => {
  return (
    <Box>
      <Typography variant="body2" align="left">
        {props.row.ab_name}
      </Typography>
      <Typography variant="caption" align="left" component="div">
        {props.row.ab_id}
      </Typography>
    </Box>
  );
};

const RenderTargetAntigenAndSpecies = (props: GridRenderCellParams<String>) => {
  return (
    <Box>
      <Typography variant="body2">
        {props.row.ab_target} {props.row.target_species}
      </Typography>
    </Box>
  );
};

const columnsDefaultProps = {
  flex: 1,
  headerAlign: "center" as GridAlignment,
  align: "center" as GridAlignment,
};

const columns: GridColDef[] = [
  {
    ...columnsDefaultProps,
    field: "ab_name",
    headerName: "Name",
    flex: 1,
    hide: true,
  },
  {
    ...columnsDefaultProps,
    field: "ab_id",
    headerName: "ID",
    flex: 1,
    hide: true,
  },
  {
    ...columnsDefaultProps,
    field: "ab_name_id",
    headerName: "Name & ID",
    flex: 2,
    renderCell: RenderNameAndId,
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
    renderCell: RenderTargetAntigenAndSpecies,
    flex: 1.5,
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
  },
  {
    ...columnsDefaultProps,
    field: "clone_id",
    headerName: "Clone ID",
    flex: 1,
  },
  {
    ...columnsDefaultProps,
    field: "host",
    headerName: "Host organism",
    flex: 1,
  },
  {
    ...columnsDefaultProps,
    field: "vendor",
    headerName: "Link to Vendor",
    flex: 2,
  },
  {
    ...columnsDefaultProps,
    field: "catalog_num",
    headerName: "Cat Num",
    flex: 1,
  },
];

function AntibodiesTable() {
  const [antibodiesList, setAntibodiesList] = useState([]);

  const fetchAntibodies = () => {
    getAntibodies()
      .then((res) => {
        return setAntibodiesList(res);
      })
      .catch((err) => alert(err));
  };

  useEffect(fetchAntibodies, []);

  return (
    <Box sx={{ height: "80vh" }}>
      <Box
        sx={(theme) => ({
          display: "flex",
          height: "100%",
          "& .MuiDataGrid-columnHeadersInner": {
            backgroundColor: theme.palette.grey[50],
          },
        })}
      >
        <Box sx={{ flexGrow: 1 }}>
          <DataGrid
            rows={antibodiesList}
            columns={columns}
            pageSize={20}
            rowsPerPageOptions={[20]}
            checkboxSelection
            disableSelectionOnClick
            components={{ Toolbar: GridToolbar }}
            getRowHeight={() => "auto"}
          />
        </Box>
      </Box>
    </Box>
  );
}

export default AntibodiesTable;
