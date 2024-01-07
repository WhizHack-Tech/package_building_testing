// ** React Imports
import { useState } from 'react'
import { Link } from 'react-router-dom'
// ** Table columns & Expandable Data
import ExpandableTable, { Columns } from './data'
import { useSelector } from 'react-redux'
import { useTranslation } from 'react-i18next'
// ** Third Party Components
import ReactPaginate from 'react-paginate'
import { ChevronDown, Info } from 'react-feather'
import DataTable from 'react-data-table-component'
import { Card, CardHeader, CardTitle, Popover, PopoverHeader, PopoverBody, Badge } from 'reactstrap'

const DataTableWithButtons = () => {
  // ** State
  const { t } = useTranslation()
  const [currentPage, setCurrentPage] = useState(0)
  const [popoverOpen, setPopoverOpen] = useState(false)

  const TestPageTable = useSelector((store) => store.test_page.charts)
  const chart_length = Object.keys(TestPageTable).length
  let table_length = 0
  if (chart_length > 0) {
    table_length = Object.keys(TestPageTable.TestPageTable).length
  }

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
      pageCount={table_length}
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
      {/* <div style={{ height: '680px' }}> */}
      <CardHeader>
        <CardTitle tag='h4'>{t('Threat Logs')}</CardTitle>
        <Badge color='primary'>
          <Link><Info id='Detection_Data' size={20} /></Link>
        </Badge>
        <Popover
          placement='top'
          target='Detection_Data'
          isOpen={popoverOpen}
          toggle={() => setPopoverOpen(!popoverOpen)}
        >
          <PopoverHeader>{t('Threat Logs')}</PopoverHeader>
          <PopoverBody>
            {t('Threat logs display entries when traffic matches one of the Security Profiles attached to a security filter by the Triple Layered Detection Engine')}
          </PopoverBody>
        </Popover>
      </CardHeader>
      <DataTable
        noHeader
        pagination
        data={(chart_length > 0) ? TestPageTable.TestPageTable : []}
        expandableRows
        columns={Columns()}
        expandOnRowClicked
        className='react-dataTable'
        sortIcon={<ChevronDown size={10} />}
        paginationDefaultPage={currentPage + 1}
        expandableRowsComponent={<ExpandableTable />}
        paginationRowsPerPageOptions={[10, 25, 50, 100]}
      // paginationComponent={CustomPagination}
      />
      {/* </div> */}
    </Card>
  )
}

export default DataTableWithButtons