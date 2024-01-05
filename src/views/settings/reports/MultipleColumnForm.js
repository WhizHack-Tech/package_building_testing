// ================================================================================================
//  File Name: MultipleColumnForm.js
//  Description: Details of the Static Report Page.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Card, Spinner, CardHeader, CardTitle, CardBody, FormGroup, Row, Col, Input, Form, Button, Label } from 'reactstrap'
import { useState, Fragment, useEffect, useRef } from 'react'
import 'flatpickr/dist/flatpickr.css'
import axios from '@axios'
import { token, selectThemeColors } from '@utils'
import { format } from "date-fns"
import { toast } from 'react-toastify'
import ExportTablesBasic from "./export"
import { useTranslation } from 'react-i18next'
import Select from 'react-select'
import { useSelector } from "react-redux"
import PreLoader from './preLoader'
import { selectOptionFormat } from '../../../utility/helpers'

const logsTyps = [
  { value: 'alert', label: 'Alert', color: '#00B8D9', isFixed: true },
  { value: 'event', label: 'Event', color: '#0052CC', isFixed: true },
  { value: 'incident', label: 'Incident', color: '#5243AA', isFixed: true }
  // { value: 'dpi', label: 'DPI', color: '#5243AA', isFixed: true }
]
const platform = [
  { value: 'aws', label: 'AWS', color: '#00B8D9', isFixed: true },
  { value: 'azure', label: 'Azure', color: '#0052CC', isFixed: true },
  { value: 'onpremise', label: 'On-Prim', color: '#5243AA', isFixed: true }
]

const MultipleColumn = () => {
  const { t } = useTranslation()
  const [startDatePicker, setStartDatePicker] = useState(new Date())
  const [endDatePicker, setEndDatePicker] = useState(new Date())
  const [loading, setLoading] = useState(false)
  const [apiData, setApiData] = useState([])
  const [urlReport, setUrlReport] = useState("")
  const { env_trace, env_nids, env_hids } = useSelector((store) => store.pagesPermissions)
  const [threatDisabled, setThreatDisabled] = useState(false)
  const [traceDisabled, setTraceDisabled] = useState(false)
  const [traceApiData, setTraceApiData] = useState(false)
  const resetSelect = useRef()

  //get product type from pagesPermissions coditions.
  const productTypes = []

  if (env_trace) {
    productTypes.push({ value: 'trace', label: 'TRACE', color: '#00B8D9', isFixed: true })
  }

  if (env_nids) {
    productTypes.push({ value: 'nids', label: 'NIDS', color: '#00B8D9', isFixed: true })
  }

  if (env_hids) {
    productTypes.push({ value: 'hids', label: 'HIDS', color: '#00B8D9', isFixed: true })
  }

  const productInputHandle = (event) => {

    // Disabled logic for threat type #START
    setThreatDisabled(event.value === 'hids')
    setTraceDisabled(event.value === 'trace')
    resetSelect.current.state.value = []
    // Disabled logic for threat type #END

  }

  const formSubmit = (event) => {

    event.preventDefault()
    const formData = new FormData(event.target)
    let start_date = new Date()
    let end_date = new Date()
    if (startDatePicker.length > 0 && startDatePicker[0] !== "") {
      start_date = startDatePicker[0]
    }

    if (endDatePicker.length > 0 && endDatePicker[0] !== "") {
      end_date = endDatePicker[0]
    }

    start_date = format(start_date, "yyyy-MM-dd")
    end_date = format(end_date, "yyyy-MM-dd")

    formData.append("start_date", start_date)
    formData.append("end_date", end_date)
    setLoading(true)
    axios(urlReport, {
      method: "post",
      data: formData,
      headers: { Authorization: token() }
    }).then(res => {
      setLoading(false)
      if (res.data.message_type === "data_ok") {
        setApiData(res.data.data)
      } else {
        setApiData([])
      }

      if (res.data.message_type === "d_not_f") {
        toast.info(t('Requested data not available'), {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined
        })
      }
    }).catch(error => {
      setLoading(false)
    })
  }

  const RenderExportTable = () => {
    return <CardBody> {apiData.length > 0 ? <ExportTablesBasic data={apiData} /> : <p className='text-center mt-2'>{t('Data Not Found')}</p>} </CardBody>
  }

  const traceDataApi = () => {
    axios.get("/get-trace-sensor-names", { headers: { Authorization: token() } })
      .then(res => {
        if (res.data.message_type === "d_found") {
          setTraceApiData(selectOptionFormat(res.data.data))
        }
      })
      .catch(err => {
        console.log(err.message)
      })
  }

  useEffect(() => {
    traceDataApi()
  }, [])

  return (
    <Fragment>
      <Card>
        <CardHeader>
          <CardTitle tag='h2'>{t('Filter')}</CardTitle>
        </CardHeader>
        <CardBody>
          <Form onSubmit={formSubmit}>
            <Row>
              <Col className='mb-1' md='6' sm='12'>
                <Label>Product Types</Label>
                <Select
                  isClearable={false}
                  theme={selectThemeColors}
                  placeholder={<div className="select-placeholder-text" style={{ color: "#a5a7af" }}>Select...</div>}
                  name='product_types'
                  options={productTypes}
                  className='react-select'
                  classNamePrefix='select'
                  onChange={productInputHandle}
                  required 
                />
              </Col>
              <Col md='6' sm='12'>
                <FormGroup>
                  <Label>{t('Select Subject')}</Label>
                  <Input type='select' required onChange={(e) => {
                    setUrlReport(e.target.value)
                  }} >
                    <option value='' selected disabled>Report Type</option>
                    <option value='/incident-response-report'>Incident Response Report</option>
                    <option value='/executive-report'>Executive Report</option>
                  </Input>
                </FormGroup>
              </Col>
              {traceDisabled === false ? (<Col className='mb-1' md='6' sm='12'>
                <Label>{t('Select Platform')}</Label>
                <Select
                  isClearable={true}
                  theme={selectThemeColors}
                  placeholder={<div className="select-placeholder-text" style={{ color: "#a5a7af" }}>Select...</div>}
                  color="red"
                  isMulti
                  name='platform'
                  options={platform}
                  className='react-select'
                  classNamePrefix='select' 
                  ref={resetSelect}
                />
              </Col>) : (<Col className='mb-1' md='6' sm='12'>
                <Label>{t('Trace Sensor Names')}</Label>
                <Select
                  isClearable={true}
                  theme={selectThemeColors}
                  placeholder={<div className="select-placeholder-text" style={{ color: "#a5a7af" }}>Select...</div>}
                  color="red"
                  isMulti
                  name='sensor_names'
                  options={traceApiData}
                  className='react-select'
                  classNamePrefix='select'
                  ref={resetSelect}
                />
              </Col>)}

              <Col md='6' sm='12'>
                <FormGroup>
                  <Label>{t('Type of Threat')}</Label>
                  <Input type='select' name='threat_type' required disabled={threatDisabled}>
                    <option value='' selected disabled>Select...</option>
                    <option value='internal_attack'>Internal</option>
                    <option value='external_attack'>External</option>
                  </Input>
                </FormGroup>
              </Col>
              <Col md='6' sm='12'>
                <FormGroup>
                  <Label>{t('Select Count')}</Label>
                  <Input type='select' name='top_count' required >
                    <option value='' selected disabled>Select..</option>
                    <option value='10'>Top-10</option>
                    <option value='20'>Top-20</option>
                    <option value='50'>Top-50</option>
                    <option value='100'>Top-100</option>
                    {/* <option value=''>All</option> */}
                  </Input>
                </FormGroup>
              </Col>
              <Col className='mb-1' md='6' sm='12'>
                <Label>Logs Type</Label>
                <Select
                  isClearable={false}
                  theme={selectThemeColors}
                  placeholder={<div className="select-placeholder-text" style={{ color: "#a5a7af" }}>Select...</div>}
                  name='logs_type'
                  options={logsTyps}
                  className='react-select'
                  classNamePrefix='select'
                />
              </Col>
              <Col className='mb-1' md='6' sm='12'>
                <FormGroup>
                  <Label>Filter Range</Label>
                  <Input type='select' name='condition' required >
                    <option value='' selected disabled>Select...</option>
                    <option value='last_5_minutes'>Last 5 minutes</option>
                    <option value='last_15_minutes'>Last 15 minutes</option>
                    <option value='last_30_minutes'>Last 30 minutes</option>
                    <option value='last_1_hour'>Last 1 Hour</option>
                    <option value='last_6_hours'>Last 6 Hours</option>
                    <option value='last_12_hours'>Last 12 Hours</option>
                    <option value='last_24_hours'>Last 24 Hours</option>
                    <option value='last_7_days'>Last 7 Days</option>
                    <option value='last_15_days'>Last 15 Days</option>
                    <option value='last_30_days'>Last 30 Days</option>
                  </Input>
                </FormGroup>
              </Col>
              <Col sm='6'>
                <FormGroup className='d-flex mt-2'>
                  <div className='mr-1'>
                    {(loading === false) ? <Button.Ripple color='primary' type="submit">{t('Generate Report')}</Button.Ripple> : <Button.Ripple type="button" color='primary' disabled> <Spinner size="sm" />&nbsp;{t('Checking')}...</Button.Ripple>}
                  </div>
                </FormGroup>
              </Col>
            </Row>
          </Form>
        </CardBody>
      </Card>

      <Card>
        <RenderExportTable />
        {loading && <PreLoader />}
      </Card>
    </Fragment>
  )
}
export default MultipleColumn