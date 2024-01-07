import Timeline from '@components/timeline'
import {
  Card,
  CardBody,
  CardHeader,
  CardTitle,
  Spinner,
  Label,
  Input,
  Row,
  Col,
  Alert
} from 'reactstrap'
import { useState, useEffect } from 'react'
import axios from '@axios'
import { Activity } from 'react-feather'
import '@styles/react/apps/app-email.scss'
import { useTranslation } from 'react-i18next'
import { format } from 'date-fns'
// ** Utils
import { token } from '@utils'

let scrollPosition = 1318 // value of div height
let scrollPositionIncrement = 1318 // value of div height
const scrollPositionLimit = 10
let scrollPositionOffset = 0
const logData = []

const BasicTimeline = () => {
  const { t } = useTranslation()
  const [cardLogs, setCardLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchValue, setSearchValue] = useState('')
  const [filteredData, setFilteredData] = useState([])

  function logApi(limit, offset = 0) {
    setLoading(true)
    axios
      .get(`/client-logs?limit=${limit}&offset=${offset}`, {
        headers: { Authorization: token() }
      })
      .then((res) => {
        if (res.data.message_type === 'data_found') {
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
    if (
      event.target.scrollHeight - event.target.scrollTop ===
        scrollPosition &&
      loading
    ) {
      scrollPosition = (scrollPosition += scrollPositionIncrement)
      scrollPositionOffset = (scrollPositionOffset += scrollPositionLimit)

      logApi(scrollPositionLimit, scrollPositionOffset)
      scrollPositionIncrement = event.target.clientHeight
    }
  }

  useEffect(() => {
    const scrollBox = document.querySelector('.logTableScrollRef')
    if (scrollBox) {
      scrollBox.addEventListener('scroll', handleScroll, { passive: true })
      logApi(scrollPositionLimit)
    }

    return () => {
      // Remove the event listener when the component unmounts to prevent memory leaks
      if (scrollBox) {
        scrollBox.removeEventListener('scroll', handleScroll)
      }
    }
  }, [])

  const handleFilter = (e) => {
    const value = e.target.value
    setSearchValue(value)

    let updatedData = []

    if (value.length) {
      updatedData = cardLogs.filter((item) => {
        const startsWith =
          item.browser_type
            .toLowerCase()
            .startsWith(value.trim().toLowerCase()) ||
          item.date_time
            .toLowerCase()
            .startsWith(value.trim().toLowerCase()) ||
          item.description
            .toLowerCase()
            .startsWith(value.trim().toLowerCase()) ||
          item.ip.toLowerCase().startsWith(value.trim().toLowerCase()) ||
          item.username
            .toLowerCase()
            .startsWith(value.trim().toLowerCase()) ||
          item.req_method
            .toLowerCase()
            .startsWith(value.trim().toLowerCase()) ||
          item.email.toLowerCase().startsWith(value.trim().toLowerCase()) ||
          item.type.toLowerCase().startsWith(value.trim().toLowerCase())

        const includes =
          item.browser_type
            .toLowerCase()
            .includes(value.trim().toLowerCase()) ||
          item.date_time
            .toLowerCase()
            .includes(value.trim().toLowerCase()) ||
          item.description
            .toLowerCase()
            .includes(value.trim().toLowerCase()) ||
          item.ip.toLowerCase().includes(value.trim().toLowerCase()) ||
          item.username
            .toLowerCase()
            .includes(value.trim().toLowerCase()) ||
          item.req_method
            .toLowerCase()
            .includes(value.trim().toLowerCase()) ||
          item.email.toLowerCase().includes(value.trim().toLowerCase()) ||
          item.type.toLowerCase().includes(value.trim().toLowerCase())

        return startsWith || includes
      })
    }

    setFilteredData(updatedData)
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
      meta: (
        <Alert color='primary' className='text-uppercase'>
          {format(new Date(data.date_time), 'yyyy-MM-dd, h:mm:ss a')}
        </Alert>
      ),
      username: `Username : ${data.email}`,
      color: data.color
    }
  })

  return (
    <Card>
      <CardHeader>
        <CardTitle tag='h5' className='mt-0 mb-0'>
          {t('User Logs')}
        </CardTitle>
        <Row className='justify-content-end mx-0'>
          <Col
            className='d-flex align-items-center justify-content-end mt-1'
            style={{ width: '25rem' }}
            md='12'
          >
            <Label className='mr-1' for='search-input'>
              {t('Search')}
            </Label>
            <Input
              className='dataTable-filter mb-50'
              type='text'
              bsSize='sm'
              id='search-input'
              value={searchValue}
              // onChange={(e) => setSearchValue(e.target.value)}
              onChange={(e) => setSearchValue(e.target.value.trim())}
              onKeyUp={handleFilter}
            />
          </Col>
        </Row>
      </CardHeader>
      <hr className='m-0' />
      <div className='scroll-box logTableScrollRef p-0'>
        {loading ? (
          <div
            style={{
              backgroundColor: 'transparent',
              position: 'absolute',
              width: '100%',
              height: '100%',
              zIndex: 99999,
              paddingTop: '20rem'
            }}
            className='d-flex justify-content-center'
          >
            <Spinner animation='border' type='grow' color='primary' />
          </div>
        ) : (
          ''
        )}
        <CardBody>
          <Timeline data={dataRenderLogs} />
        </CardBody>
      </div>
   </Card>
  )
}

export default BasicTimeline
