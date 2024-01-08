// ================================================================================================
//  File Name: ApiKey.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
// ** React Imports
import { useState, useEffect, useRef, Fragment } from 'react'
// ** Third Party Components
import ReactPaginate from 'react-paginate'
import { ChevronDown, Download } from 'react-feather'
import DataTable from 'react-data-table-component'
import axios from '@axios'
import { token } from '@utils'
import { useSelector } from 'react-redux'
import PreLoader from '../preLoader'
// ** Reactstrap Imports
import { Card, CardHeader, CardTitle, Badge, Nav, NavItem, NavLink, TabContent, TabPane, Row, Col, Button, Input, Label } from 'reactstrap'
import { jsPDF } from 'jspdf'
import 'jspdf-autotable'
import "./pdfStyles.css"
import { useTranslation } from 'react-i18next'

const DataTableWithButtons = () => {
  // ** State
  const { t } = useTranslation()
  const [currentPage, setCurrentPage] = useState(0)
  const [apiLoader, setApiLoader] = useState(false)
  const [tableData, setTableData] = useState([])
  const filterState = useSelector((store) => store.dashboard_chart)
  const [searchQuery, setSearchQuery] = useState('')

  const DetailsApiLogic = () => {
    setApiLoader(true)
    axios.get(`/glog-trace-logs-table?condition=${filterState.values ? filterState.values : 'last_90_days'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)

        if (res.data.message_type === "success") {
          setTableData(res.data.data)
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


 const handleDownloadPDF = (rowData) => {
  if (!rowData) {
    console.log('rowData is null or undefined:', rowData)
    return
  }

  console.log('rowData:', rowData)

  const doc = new jsPDF()

  const {
    attack_timestamp,
    intel_source
  } = rowData

  doc.setFont('helvetica', 'bold')
  doc.setFontSize(16)
  const headingText = 'Gobal Trace Details'
  const textWidth = (doc.getStringUnitWidth(headingText) * doc.internal.getFontSize()) / doc.internal.scaleFactor
  const textOffset = (doc.internal.pageSize.width - textWidth) / 2

  doc.text(headingText, textOffset, 20)
  doc.setFont('Arial', 'normal')
  doc.setFontSize(11)
  doc.setTextColor(255, 0, 0)
  doc.text('Timestamp :', 10, 40)
  doc.text('Intel Source :', 10, 50)

  // Add null checks for other properties before accessing them
  doc.setTextColor(0)
  doc.text(attack_timestamp !== undefined && attack_timestamp !== null ? attack_timestamp.toString() : '', 50, 40)
  doc.text(intel_source !== undefined && intel_source !== null ? intel_source.toString() : '', 50, 50)

  doc.save('Gobal Trace Details.pdf')
}

  const CustomDownloadButton = ({ data }) => (
    <Button.Ripple color='flat-primary' size='sm' className="btn btn-sm" onClick={() => handleDownloadPDF(data)}>
      <Download size={16} />
    </Button.Ripple>
  )

  const filteredData = tableData.filter((row) => Object.values(row).some((value) => {
    return value !== null ? value.toString().toLowerCase().includes(searchQuery.toLowerCase()) : ''
  }))


  const handleSearch = (e) => {
    setSearchQuery(e.target.value)
  }


  const Columns = [
    {
      name: 'Product',
      sortable: true,
      selector: row => row.attack_timestamp,
      wrap: true,
      width: "200px"
    },
    {
      name: 'Key',
      sortable: true,
      selector: row => row.malware_detail,
      wrap: true,
      width: "250px"
    },
    {
      name: t('Download'),
      selector: null,
      sortable: true,
      Width: '150px',
      cell: row => <CustomDownloadButton data={row} />
    }
  ]
  return (
    <Card>
      <CardHeader>
        <CardTitle className='fw-bolder' tag='h4'>{t('Global Threat Feed')}</CardTitle>
        <Col className='d-flex align-items-center justify-content-end mt-1' md='6' sm='12'>
            <Label className='me-1' for='search-input'>
              {t('Search')}
            </Label>
            <Input
              className='dataTable-filter mb-50'
              type='text'
              bsSize='sm'
              id='search-input'
              value={searchQuery}
              onChange={handleSearch}
              placeholder='Search...'
            />
          </Col>
      </CardHeader>
      <div className='react-dataTable'>
          <DataTable
            noHeader
            pagination
            data={filteredData}
            expandableRows
            columns={Columns}
            paginationPerPage={10}
            expandOnRowClicked
            className='react-dataTable'
            sortIcon={<ChevronDown size={10} />}
            paginationDefaultPage={currentPage + 1}
            expandableRowsComponent={ExpandableTable}
            paginationRowsPerPageOptions={[10, 25, 50, 100]}
          />
      </div>
    </Card>
  )
}

export default DataTableWithButtons
