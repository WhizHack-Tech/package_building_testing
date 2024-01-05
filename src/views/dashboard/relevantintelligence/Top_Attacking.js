// ** React Imports
import { Fragment, useState, forwardRef } from 'react'

// ** Table Data & Columns
import { data, Ip } from './data1'

// ** Add New Modal Component
// import AddNewModal from './AddNewModal'
import jsPDF from 'jspdf'
import 'jspdf-autotable'
// ** Third Party Components
import XLSX from 'xlsx'
import ReactPaginate from 'react-paginate'
import { useTranslation } from 'react-i18next'
import DataTable from 'react-data-table-component'
import { useSelector } from "react-redux"
import { ChevronDown, Share, Printer, FileText, File, Grid, Copy, Plus } from 'react-feather'
import {
  Card,
  CardHeader,
  CardTitle,
  Button,
  UncontrolledButtonDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  Input,
  Label,
  Row,
  Col,
  CardSubtitle,
  Spinner
} from 'reactstrap'
import axios from 'axios'

// ** Bootstrap Checkbox Component
const BootstrapCheckbox = forwardRef(({ onClick, ...rest }, ref) => (
  <div className='custom-control custom-checkbox'>
    <input type='checkbox' className='custom-control-input' ref={ref} {...rest} />
    <label className='custom-control-label' onClick={onClick} />
  </div>
))

const DataTableWithButtons = () => {
  const {t} = useTranslation()
  const TopAttackingIPs = useSelector((store) => store.tables_charts.charts)
  const chart_length = Object.keys(TopAttackingIPs).length
  let table_length = 0
  if (chart_length > 0) {
    table_length = Object.keys(TopAttackingIPs.TopAttackingIPs).length
  }
  // ** States
  const [modal, setModal] = useState(false)
  const [currentPage, setCurrentPage] = useState(0)
  const [searchValue, setSearchValue] = useState('')
  const [filteredData, setFilteredData] = useState([])

  // ** Function to handle Modal toggle
  const handleModal = () => setModal(!modal)

  // ** Function to handle filter
  const handleFilter = e => {
    const value = e.target.value
    let updatedData = []
    setSearchValue(value)

    const status = {
      1: { title: 'Current', color: 'light-primary' },
      2: { title: 'Professional', color: 'light-success' },
      3: { title: 'Rejected', color: 'light-danger' },
      4: { title: 'Resigned', color: 'light-warning' },
      5: { title: 'Applied', color: 'light-info' }
    }

    if (value.length) {
      updatedData = data.filter(item => {
        const startsWith =
          item.attacker_ip.toLowerCase().startsWith(value.toLowerCase()) ||
          item.attacker_mac.toLowerCase().startsWith(value.toLowerCase()) 

        const includes =
          item.attacker_ip.toLowerCase().includes(value.toLowerCase()) ||
          item.attacker_mac.toLowerCase().includes(value.toLowerCase()) 

        if (startsWith) {
          return startsWith
        } else if (!startsWith && includes) {
          return includes
        } else return null
      })
      setFilteredData(updatedData)
      setSearchValue(value)
    }
  }

  // ** Function to handle Pagination
  const handlePagination = page => {
    setCurrentPage(page.selected)
  }

  // ** Custom Pagination
  const CustomPagination = () => (
    <ReactPaginate
      previousLabel=''
      nextLabel=''
      forcePage={currentPage}
      onPageChange={page => handlePagination(page)}
      pageCount={table_length / 5 || 1}
      breakLabel='...'
      pageRangeDisplayed={2}
      marginPagesDisplayed={2}
      activeClassName='active'
      pageClassName='page-item'
      breakClassName='page-item'
      breakLinkClassName='page-link'
      nextLinkClassName='page-link'
      nextClassName='page-item next'
      previousClassName='page-item prev'
      previousLinkClassName='page-link'
      pageLinkClassName='page-link'
      containerClassName='pagination react-paginate separated-pagination pagination-sm justify-content-end pr-1 mt-1'
    />
  )

  // ** Converts table to CSV
  function convertArrayOfObjectsToCSV(array) {
    let result

    const columnDelimiter = ','
    const lineDelimiter = '\n'
    const keys = Object.keys(TopAttackingIPs.TopAttackingIPs[0])

    result = ''
    result += keys.join(columnDelimiter)
    result += lineDelimiter

    array.forEach(item => {
      let ctr = 0
      keys.forEach(key => {
        if (ctr > 0) result += columnDelimiter

        result += item[key]

        ctr++
      })
      result += lineDelimiter
    })

    return result
  }

  // ** Downloads CSV
  function downloadCSV(array) {
    const link = document.createElement('a')
    let csv = convertArrayOfObjectsToCSV(array)
    if (csv === null) return

    const filename = 'Attacker Details.csv'

    if (!csv.match(/^TopAttackingIPs.TopAttackingIPs:text\/csv/i)) {
      csv = `data:text/csv;charset=utf-8,${csv}`
    }

    link.setAttribute('href', encodeURI(csv))
    link.setAttribute('download', filename)
    link.click()
  }
    // ** download PDF
    const downloadPdf = () => {
      let dataArr = []
  
      if (table_length > 0) {
        dataArr = TopAttackingIPs.TopAttackingIPs.map(rowData => {
          return [rowData.attacker_ip, rowData.attacker_mac, rowData['count(attacker_ip)']]
        })
      }
  
      const doc = new jsPDF()
      doc.text("Attacker Details", 14, 10)
      doc.autoTable({
        theme: "striped",
        head: [['Attacker IPs', 'Attacker Mac Address', 'No Of Times Attacked']],
        body:  dataArr
      })
      doc.save('Attacker Details.pdf')
    }
    // ** download xlsx
    const downloadExcel = () => {
      const newData = TopAttackingIPs.TopAttackingIPs.map(row => {
        delete row.tableData
        return row
      })
      const workSheet = XLSX.utils.json_to_sheet(newData)
      const workBook = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(workBook, workSheet, "students")
      //Buffer
      XLSX.write(workBook, { bookType: "xlsx", type: "buffer" })
      //Binary string
      XLSX.write(workBook, { bookType: "xlsx", type: "binary" })
      //Download
      XLSX.writeFile(workBook, "Attacker Details.xlsx")
  
  
    }

  return (
    <Fragment>
      <Card>
        <CardHeader className='flex-md-row flex-column align-md-items-center align-items-start border-bottom'>
        <div>
          <CardTitle className='mb-75' tag='h4'>
          {t('Attacker Details')}
          </CardTitle>
          </div>
          <div className='d-flex mt-md-0 mt-1'>
            <UncontrolledButtonDropdown>
              <DropdownToggle color='secondary' caret outline>
                <Share size={15} />
                <span className='align-middle ml-50'>{t('Export')}</span>
              </DropdownToggle>
              <DropdownMenu right>
                <DropdownItem className='w-100' onClick={() => downloadCSV(TopAttackingIPs.TopAttackingIPs)}>
                  <FileText size={15} />
                  <span className='align-middle ml-50'>{t('CSV')}</span>
                </DropdownItem>
                <DropdownItem className='w-100' onClick={() => downloadExcel(TopAttackingIPs.TopAttackingIPs)}>
                  <Grid size={15} />
                  <span className='align-middle ml-50'>{t('Excel')}</span>
                </DropdownItem>
                <DropdownItem className='w-100' onClick={() => downloadPdf(TopAttackingIPs.TopAttackingIPs)}>
                  <Grid size={15} />
                  <span className='align-middle ml-50'>{t('PDF')}</span>
                </DropdownItem>
              </DropdownMenu>
            </UncontrolledButtonDropdown>
            </div>
        </CardHeader>
         <DataTable
          noHeader
          pagination
          columns={Ip()}
          paginationPerPage={5}
          className='react-dataTable'
          paginationDefaultPage={currentPage + 1}
          paginationComponent={CustomPagination}
          data={searchValue.length ? filteredData : TopAttackingIPs.TopAttackingIPs}
          selectableRowsComponent={BootstrapCheckbox}
        />
      </Card>
      {/* <AddNewModal open={modal} handleModal={handleModal} /> */}
    </Fragment>
  )
}

export default DataTableWithButtons
