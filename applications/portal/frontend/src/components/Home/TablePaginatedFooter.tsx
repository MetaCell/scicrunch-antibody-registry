import React, { useContext } from "react";
import { IconButton } from "@mui/material";
import { ChevronLeft, ChevronRight } from '@mui/icons-material'
import { PAGE_SIZE } from "../../constants/constants";
import { debounce } from 'lodash';
import SearchContext from "../../context/search/SearchContext";

export const TablePaginatedFooter = () => {
  const { totalElements, currentPage, setCurrentPage } = useContext(SearchContext);

  const handleNextPage = debounce(() => {
    setCurrentPage(currentPage + 1)
  }, 800)

  const handlePrevPage = debounce(() => {
    setCurrentPage(currentPage - 1)
  }, 800)

  const startPageCount = totalElements ? (currentPage - 1) * PAGE_SIZE + 1 : 0;
  const endPageCount = totalElements ? (currentPage * PAGE_SIZE > totalElements ? totalElements : currentPage * PAGE_SIZE) : 0;
  return (
    <div style={{ display: "flex", justifyContent: "flex-end", alignItems: "center", marginTop: '1rem' }}>
      <div>
        {startPageCount}-
        {endPageCount} {' '}
        of {totalElements} results
      </div>
      <div>
        <IconButton style={{ cursor: 'pointer' }} onClick={() => handlePrevPage()} disabled={currentPage <= 1}>
          <ChevronLeft />
        </IconButton>
        <IconButton style={{ cursor: 'pointer' }} onClick={() => handleNextPage()} disabled={currentPage >= Math.ceil(totalElements / PAGE_SIZE)}>
          <ChevronRight />
        </IconButton>

      </div>
    </div>
  )
}