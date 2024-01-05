// ** React Imports
import { useState, useEffect } from 'react'

// ** Table columns & Expandable Data
import ExpandableTable, { columns } from './data'

// ** Third Party Components
import ReactPaginate from 'react-paginate'
import { ChevronDown } from 'react-feather'
import DataTable from 'react-data-table-component'
import { Card, CardHeader, CardTitle } from 'reactstrap'
import axios from '@axios'
import PreLoader from '../preLoader'
import { useSelector } from 'react-redux'
const DataTableWithButtons = () => {
  // ** State
  const [currentPage, setCurrentPage] = useState(0)
  const [apiLoader, setApiLoader] = useState(false)
  const [tableData, setTableData] = useState([])
  const filterState = useSelector((store => store.dashboard_chart))

  const DetailsApiLogic = () => {
      setApiLoader(true)
      axios.get(`/nids-dashboard-threat-logs?condition=${filterState.values ? filterState.values : 'today'}`)
          .then(res => {
              setApiLoader(false)
              if (res.data.message_type === "success") {
                  setTableData(res.data.threat_logs)
              }
          })
          .catch(error => {
              setApiLoader(false)
              console.log(error.message)
          })
  }

  useEffect(() => {
      DetailsApiLogic()
  }, [filterState.values, filterState.refreshCount])

  // ** Function to handle filter
  const handlePagination = page => {
    setCurrentPage(page.selected)
  }

  // ** Custom Pagination
  const CustomPagination = () => (
    <ReactPaginate
      previousLabel={''}
      nextLabel={''}
      forcePage={currentPage}
      onPageChange={page => handlePagination(page)}
      pageCount={13}
      breakLabel={'...'}
      pageRangeDisplayed={2}
      marginPagesDisplayed={2}
      activeClassName={'active'}
      pageClassName={'page-item'}
      nextLinkClassName={'page-link'}
      nextClassName={'page-item next'}
      previousClassName={'page-item prev'}
      previousLinkClassName={'page-link'}
      pageLinkClassName={'page-link'}
      breakClassName='page-item'
      breakLinkClassName='page-link'
      containerClassName={'pagination react-paginate separated-pagination pagination-sm justify-content-end pr-1'}
    />
  )

  return (
    <Card>
      <CardHeader>
        <CardTitle tag='h4'>Threat Logs</CardTitle>
      </CardHeader>
      <DataTable
        noHeader
        pagination
        data={tableData}
        expandableRows
        columns={columns}
        expandOnRowClicked
        className='react-dataTable'
        sortIcon={<ChevronDown size={10} />}
        paginationDefaultPage={currentPage + 1}
        expandableRowsComponent={<ExpandableTable />}
        paginationRowsPerPageOptions={[10, 25, 50, 100]}
        paginationComponent={CustomPagination}
      />

{apiLoader ? <PreLoader /> : null}
    </Card>
  )
}

export default DataTableWithButtons
