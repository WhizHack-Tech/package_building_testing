// ================================================================================================
//  File Name: tableData.js
//  Description: Details of the Health Check ( Health Check Logs ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** React Imports
import { useState, Fragment } from 'react'
import { ChevronDown } from 'react-feather'
import DataTable from 'react-data-table-component'

import { Card, CardHeader, CardTitle, Nav, NavItem, NavLink, TabContent, TabPane, Row, Col, Input, Label, Badge, Progress } from 'reactstrap'
import { useTranslation } from 'react-i18next'
import { RadialBarChart, RadialBar, Legend } from 'recharts'
import RamUtilizationProgressBar from '../charts/LineChart/Circle'
import Download from '../charts/LineChart/Circle2'

const TableDataRender = ({ tableData }) => {

  const { t } = useTranslation()
  const [searchQuery, setSearchQuery] = useState('')

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

  const filteredData = tableData.filter((row) => Object.values(row).some((value) => {
    return value !== null ? value.toString().toLowerCase().includes(searchQuery.toLowerCase()) : ''
  }))


  const handleSearch = (e) => {
    setSearchQuery(e.target.value)
  }
  

  const columnsName = [
    {
      name: t('Timestamp'),
      sortable: true,
      selector: row => row.timestamp,
      wrap: true,
      width: "200px"
    },
    {
      name: t('Log Info'),
      sortable: true,
      wrap: true,
      cell: (row) => ((row.level === "running") ? <Badge color="success">{row.level}</Badge> : <Badge color="danger">{row.level}</Badge>)
    },
    {
      name: t("Sensor ID"),
      sortable: true,
      selector: row => row.sensor_id,
      wrap: true
    },
    {
      name: t("IP Address"),
      sortable: true,
      width: "150px",
      selector: row => row.ip_address,
      wrap: true
    },
    {
      name: t("Disk Remaining"),
      sortable: true,
      wrap: true,
      cell: (row) => (
        <div className='demo-vertical-spacing w-100'>
          <Progress value={row.disk_remaining} className='progress-bar-warning'>
            {row.disk_remaining}
          </Progress>
        </div>
      ),
      width: "200px"
    },
    {
      name: t("CPU Utilization"),
      sortable: true,
      wrap: true,
      cell: (row) => (
        <div className='demo-vertical-spacing w-100'>
          <Progress value={row.cpu_utilization} className='progress-bar-danger'>
            {row.cpu_utilization}
          </Progress>
        </div>
      ),
      width: "200px"
    },
    {
      name: t("RAM Utilization"),
      sortable: true,
      wrap: true,
      cell: (row) => (
        <div className='demo-vertical-spacing w-100'>
          <Progress value={row.ram_utilization} className='progress-radialBar-primary'>
            {row.ram_utilization}
          </Progress>
        </div>
      ),
      width: "200px"
    },
    {
      name: t("Disk Log Details"),
      sortable: true,
      selector: row => row.disk_action,
      wrap: true
    },
    {
      name: t("Sensor Name"),
      sortable: true,
      selector: row => row.sensor_name,
      wrap: true,
      width: "250px"
    },
    {
      name: t('Upload Speed'),
      sortable: true,
      wrap: true,
      width: '180px',
      cell: (row) => (
        <div className='demo-vertical-spacing w-100'>
          <RamUtilizationProgressBar ramUtilization={row.upload_speed} />
        </div>
      )
    },
    {
      name: t('Download Speed'),
      sortable: true,
      wrap: true,
      width: '180px',
      cell: (row) => (
        <div className='demo-vertical-spacing w-100'>
          <Download download_speed={row.download_speed} />
        </div>
      )
    }
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle className='fw-bolder' tag='h4'>{t('Health Check Logs')}</CardTitle>
        <Col className='d-flex align-items-center justify-content-end mt-1' md='6' sm='12'>
          <Label className='me-1' for='search-input'>
            {t('Search')}&nbsp;&nbsp;
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
        {tableData.length > 0 ? (
          <DataTable
            noHeader
            pagination
            data={filteredData}
            expandableRows
            columns={columnsName}
            paginationPerPage={10}
            expandOnRowClicked
            className='react-dataTable'
            sortIcon={<ChevronDown size={10} />}
            expandableRowsComponent={ExpandableTable}
            paginationRowsPerPageOptions={[10, 25, 50, 100]}
          />
        ) : (
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
            <p>{t('Data Not Found')}</p>
          </div>
        )}
      </div>
    </Card>
  )
}

export default TableDataRender
