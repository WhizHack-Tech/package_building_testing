// ================================================================================================
//  File Name: masterLogs.js
//  Description: Details of the Administration ( Master Log Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import Timeline from '@components/timeline'
import { Card, CardBody, CardHeader, CardTitle, Spinner, Label, Input, Row, Col, Alert } from 'reactstrap'
import { useState, useEffect } from 'react'
import axios from '@axios'
import { Activity } from 'react-feather'
import '@styles/react/apps/app-email.scss'
import { format } from 'date-fns'
import "../user/Loader.css"
// ** Utils
import { token } from '@utils'

let scrollPosition = 630 //value of div height
let scrollPositionIncrement = 630 //value of div height
const scrollPositionLimit = 10
let scrollPositionOffset = 10
const logData = []

const MasterLogs = () => {
  const [cardLogs, setCardLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchValue, setSearchValue] = useState('')
  const [filteredData, setFilteredData] = useState([])

  function logApi(limit, offset = 0) {
    setLoading(true)
    axios.get(`/master-logs?limit=${limit}&offset=${offset}`,
      { headers: { Authorization: token() } }
    ).then(res => {
      if (res.data.message_type === "data_found") {
        for (let i = 0; i < res.data.data.length; i++) {
          logData.push(res.data.data[i])
        }
        setCardLogs(logData)
      }
      setLoading(false)

    })
  }

  function handleScroll(event) {
    scrollPosition = event.target.clientHeight
    if ((event.target.scrollHeight - event.target.scrollTop) - 5 <= scrollPosition) {
      scrollPositionOffset = scrollPositionOffset += scrollPositionLimit
      scrollPosition = scrollPosition += scrollPositionIncrement
      logApi(scrollPositionLimit, scrollPositionOffset)
    }
  }

  useEffect(() => {
    document.querySelector(".logMasterScrollRef").addEventListener('scroll', handleScroll, { passive: true })
    logApi(scrollPositionLimit)
  }, [])

  const handleFilter = e => {
    const value = e.target.value.trim()
    let updatedData = []
    setSearchValue(value)

    if (value.length) {
      updatedData = cardLogs.filter(item => {
        const startsWith =
          item.browser_type.toLowerCase().startsWith(value.toLowerCase()) ||
          item.date_time.toLowerCase().startsWith(value.toLowerCase()) ||
          item.description.toLowerCase().startsWith(value.toLowerCase()) ||
          item.ip.toLowerCase().startsWith(value.toLowerCase()) ||
          item.email.toLowerCase().startsWith(value.toLowerCase()) ||
          item.req_method.toLowerCase().startsWith(value.toLowerCase()) ||
          item.type.toLowerCase().startsWith(value.toLowerCase())

        const includes =
          item.browser_type.toLowerCase().includes(value.toLowerCase()) ||
          item.date_time.toLowerCase().includes(value.toLowerCase()) ||
          item.description.toLowerCase().includes(value.toLowerCase()) ||
          item.ip.toLowerCase().includes(value.toLowerCase()) ||
          item.email.toLowerCase().includes(value.toLowerCase()) ||
          item.req_method.toLowerCase().includes(value.toLowerCase()) ||
          item.type.toLowerCase().includes(value.toLowerCase())

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

  const dataRender = searchValue.length ? filteredData : cardLogs

  const dataRenderLogs = dataRender.map((data) => {
    return {
      title: `Activity : ${data.description}`,
      icon: <Activity size={14} />,
      content: `Browser : ${data.browser_type}`,
      customContent: `IP : ${data.ip}`,
      method: `Method : ${data.req_method}`,
      type: `Type : ${data.type}`,
      meta: <Alert color='primary' className='text-uppercase'>{format(new Date(data.date_time), "yyyy-MM-dd, h:mm:ss a")}</Alert>,
      email: `Email ID : ${data.email}`,
      color: data.color
    }
  })

  return (
    <Card>
      <CardHeader>
        <CardTitle tag='h5' className="mt-0 mb-0">Master Logs</CardTitle>
        <Row className='justify-content-end mx-0'>
          <Col className='d-flex align-items-center justify-content-end mt-1' style={{ width: "25rem" }} md='12'>
            <Label className='mr-1' for='search-input'>
              Search
            </Label>
            <Input
              className='dataTable-filter mb-50'
              type='text'
              bsSize='sm'
              id='search-input'
              value={searchValue}
              onChange={handleFilter}
            />
          </Col>
        </Row>
      </CardHeader>
      <hr className='m-0' />
      <div className='scroll-box logMasterScrollRef p-0'>
        {loading ?    <div className='d-flex justify-content-center align-items-center' style={{ height: '210px' }}>
           <div class="tri-color-ripple-spinner">
           <div class="ripple ripple1"></div>
           <div class="ripple ripple2"></div>
         </div>
         </div> : ""
        }
        <CardBody>
          <Timeline data={dataRenderLogs} />
        </CardBody>
      </div>
    </Card>
  )
}

export default MasterLogs
