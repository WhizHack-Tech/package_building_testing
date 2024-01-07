// ================================================================================================
//  File Name: Table.js
//  Description: Details of the Trace ( Golbal Threat Feed ( Global Threat Feed ) ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

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
  const filterState = useSelector((store) => store.global_charts)
  const [checkApiData, setCheckApiData] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  const DetailsApiLogic = () => {
    setApiLoader(true)
    axios.get(`/glog-trace-logs-table?condition=${filterState.values ? filterState.values : 'last_24_hours'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)

        if (res.data.message_type === "d_not_f") {
          setCheckApiData(false)
        }

        if (res.data.message_type === "success") {
          setCheckApiData(true)
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
  }, [filterState.filter_name, filterState.refreshCount])

  const ExpandableTable = ({ data }) => {
    const [active, setActive] = useState('1')
    const ObjKeys = Object.keys(data)
    const ObjVal = Object.values(data)

    const ListTableData = () => {

      if (ObjKeys.length > 0) {
        return ObjKeys.map((values, i) => {
          return (
            <Row className="m-1" key={i}>
              <Col xs={1} md={1}>{values}</Col>: {JSON.stringify(ObjVal[i])}
            </Row>
          )
        })

      } else {
        return <p>{t('Data Not Found')}</p>
      }

    }

    const JsonRenderData = () => {

      if (ObjKeys.length > 0) {
        return <pre style={{ color: "#8177f2" }}> {JSON.stringify(data, null, '\t')} </pre>
      } else {
        return <p>{t('Data Not Found')}</p>
      }
    }


    const toggle = tab => {
      if (active !== tab) {
        setActive(tab)
      }
    }
    return (

      <Fragment>
        <div className='expandable-content'>
          <Nav tabs>
            <NavItem>
              <NavLink
                active={active === '1'}
                onClick={() => {
                  toggle('1')
                }}
              >
                {t('Table')}
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink
                active={active === '2'}
                onClick={() => {
                  toggle('2')
                }}
              >
                {t('JSON')}
              </NavLink>
            </NavItem>
          </Nav>
          <TabContent className='py-50 ml-1' activeTab={active}>
            <TabPane tabId='1'>
              <ListTableData />
            </TabPane>
            <TabPane tabId='2'>
              <JsonRenderData />
            </TabPane>
          </TabContent>
        </div>
      </Fragment>
    )
  }

 const handleDownloadPDF = (rowData) => {
  if (!rowData) {
    console.log('rowData is null or undefined:', rowData)
    return
  }

  console.log('rowData:', rowData)

  const doc = new jsPDF()

  const {
    attack_timestamp,
    intel_source,
    malware_detail,
    threat_nature,
    threat_signature,
    threat_type,
    current_status
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
  doc.text('Malware Details :', 10, 60)
  doc.text('Threat Nature :', 10, 70)
  doc.text('Threat Type :', 10, 80)
  doc.text('Current Status :', 10, 90)
  doc.text('Data Source :', 10, 100)

  // Add null checks for other properties before accessing them
  doc.setTextColor(0)
  doc.text(attack_timestamp !== undefined && attack_timestamp !== null ? attack_timestamp.toString() : '', 50, 40)
  doc.text(intel_source !== undefined && intel_source !== null ? intel_source.toString() : '', 50, 50)
  doc.text(malware_detail !== undefined && malware_detail !== null ? malware_detail.toString() : '', 50, 60)
  doc.text(threat_nature !== undefined && threat_nature !== null ? threat_nature.toString() : '', 50, 70)
  doc.text(threat_type !== undefined && threat_type !== null ? threat_type.toString() : '', 50, 80)
  doc.text(current_status !== undefined && current_status !== null ? current_status.toString() : '', 50, 90)
  doc.text(threat_signature !== undefined && threat_signature !== null ? threat_signature.toString() : '', 50, 100)

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
      name: t('Timestamp'),
      sortable: true,
      selector: row => row.attack_timestamp,
      wrap: true,
      width: "200px"
    },
    {
      name: t('Malware Details'),
      sortable: true,
      selector: row => row.malware_detail,
      wrap: true,
      width: "250px"
    },
    {
      name: t('Threat Nature'),
      sortable: true,
      selector: row => row.threat_nature,
      wrap: true,
      width: "200px"
    },
    {
      name: t('Threat Severity'),
      sortable: true,
      selector: row => row.threat_severity,
      wrap: true,
      width: "200px"
    },
    {
      name: t('Threat Type'),
      sortable: true,
      selector: row => row.threat_type,
      wrap: true,
      width: "200px"
    },
    {
      name: t('Associated Domain'),
      sortable: true,
      selector: row => row.associated_domain,
      wrap: true,
      width: "200px"
    },
    {
      name: t('Current Status'),
      sortable: true,
      selector: row => row.current_status,
      wrap: true,
      width: "150px"
    },
    {
      name: t('Intel Sourced'),
      sortable: false,
      selector: row => row.intel_source,
      wrap: true,
      width: "150px"
    },
    {
      name: t('Data Source'),
      sortable: true,
      selector: row => row.threat_signature,
      wrap: false,
      width: "500px"
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
      {/* <Row className='justify-content-end mx-0'>
          <Col className='d-flex align-items-center justify-content-end mt-1' md='6' sm='12'>
            <Label className='me-1' for='search-input'>
              Search
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
        </Row> */}
      <div className='react-dataTable'>
        {checkApiData ? (
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
        ) : (
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
            <p>{t('Data Not Found')}</p>
          </div>
        )}
      </div>
      {apiLoader ? <PreLoader /> : null}
    </Card>
  )
}

export default DataTableWithButtons
