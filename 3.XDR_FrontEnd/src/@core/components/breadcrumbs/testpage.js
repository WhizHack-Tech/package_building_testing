// ==============================================================================================
//  File Name: testpage.js
//  Description: Details of the Network-Map filter by date component.
// ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** React Imports
import { addDays, format } from "date-fns"
import { useState, useEffect } from "react"
import Flatpickr from 'react-flatpickr'
import 'flatpickr/dist/flatpickr.css'
import "react-date-range/dist/styles.css"
import "react-date-range/dist/theme/default.css"
import { test_page, test_filter } from "../../../redux/actions/charts/testpage"
import { useDispatch, useSelector } from "react-redux"
import Select, { components } from 'react-select'
import { useTranslation } from 'react-i18next'
import { selectThemeColors } from '@utils'
import Proptypes, { object } from 'prop-types'
import { Filter, ChevronsRight, RefreshCw } from 'react-feather'
import {
  Button,
  Col,
  Spinner,
  FormGroup,
  Label,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Row,
  Badge
} from 'reactstrap'

const filter_value = {
  defaultVals: { platformVal: [], accuracyVal: [] },
  platform: [],
  accuracy: [],
  start_date: "",
  end_date: ""
}

const MultipleBadge = ({ filterData, color }) => {
  if (typeof filterData === "object") {
    return filterData.map(v => {
      return <Badge color={color} className="ml-1">{v}</Badge>
    })
  } else {
    return <Badge color={color}>{filterData}</Badge>
  }
}

const BreadCrumbs = props => {
  const {t} = useTranslation()
  const dispatch = useDispatch()
  const [startDatePicker, setStartDatePicker] = useState(0)
  const [endDatePicker, setEndDatePicker] = useState(0)
  const [basicModal, setBasicModal] = useState(false)
  const loadding = useSelector((store) => store.test_page.loadding)
  const filter_val_show = useSelector((store) => store.test_page.filterValue)
  const [platform, setPlatform] = useState([])
  const [accuracy, setAccuracy] = useState(0)
  const [defaultFilter, setDefaultFilter] = useState(false)

  //validation filter option
  const [platformValid, setPlatformValid] = useState(false)
  const [accuracyValid, setAccuracyValid] = useState(false)
  const [startDateValid, setStartDateValid] = useState(false)
  const [endDateValid, setEndDateValid] = useState(false)
  const [checkPlateformVal, setCheckPlateformVal] = useState(false)
  const [checkAccuracyVal, setCheckAccuracyVal] = useState(false)

  const multiOptions = {
    platform: [
      { value: 'aws', label: 'AWS', color: '#0052CC', isFixed: true },
      { value: 'azure', label: 'Azure', color: '#0052CC', isFixed: true },
      { value: 'onpremise', label: 'On-Prim', color: '#5243AA', isFixed: true }
    ],
    accuracy: [
      { value: 1, label: 'Between 91% to 100%', color: '#0052CC', isFixed: true },
      { value: 2, label: 'Between 76% to 90%', color: '#0052CC', isFixed: true },
      { value: 3, label: 'Between 65% to 75%', color: '#5243AA', isFixed: true }
    ]
  }

  const { breadCrumbTitle } = props

  
  const platformHandle = (event) => {
    let data_1 = []
    let data_f = []
    let selected_val = []
    if (event !== null) {
      event.forEach(item => {
        data_1.push(item.value)
        data_f.push(item.label)
        selected_val.push(item)
      })
    }
    filter_value.platform = data_f
    filter_value.defaultVals.platformVal = selected_val
    setPlatform(data_1)
    setDefaultFilter(true)
    setCheckPlateformVal(true)
  }

  const accuracyHandle = (event) => {
    
    let data_2 = []
    let data_f = []
    let selected_val = []
    
    if (event !== null) {
      data_2.push(event.value)
      data_f.push(event.label)
      selected_val.push(event)
    }

    filter_value.accuracy = data_f
    filter_value.defaultVals.accuracyVal = selected_val
    setAccuracy(data_2[0])
    setDefaultFilter(true)
    setCheckAccuracyVal(true)
  }

  const filter_form = () => {
    let start_date = new Date()
    let end_date = new Date()
    let check_validate = false
   
    if (startDatePicker.length > 0 && startDatePicker[0] !== "") {
      start_date = startDatePicker[0]
      setStartDateValid(false)
    } else {
      setStartDateValid(true)
      check_validate = true
    }

    if (endDatePicker.length > 0 && endDatePicker[0] !== "") {
      end_date = endDatePicker[0]
      setEndDateValid(false)
    } else {
      setEndDateValid(true)
      check_validate = true
    }

    if (checkPlateformVal) {
      if (platform.length <= 0) {
        setPlatformValid(true)
        check_validate = true
      } else {
        setPlatformValid(false)
      }
    }

    if (checkAccuracyVal) {
      if (accuracy === undefined) {
        setAccuracyValid(true)
        check_validate = true
      } else {
        setAccuracyValid(false) 
      }
    }


    start_date = format(start_date, "yyyy-MM-dd")
    end_date = format(end_date, "yyyy-MM-dd")
    filter_value.start_date = start_date
    filter_value.end_date = end_date
    
    if (defaultFilter === true) {
      if (check_validate) {
        return false
      }

      if (checkPlateformVal === false) {
        platformHandle(filter_val_show.defaultVals.platformVal)
        dispatch(test_page({ platform: filter_val_show.defaultVals.platformSetVal, accuracy, start_date, end_date }))
        dispatch(test_filter({...filter_value, platform: filter_val_show.platform}))
      }
      
      if (checkAccuracyVal === false) {
        accuracyHandle(filter_val_show.defaultVals.accuracyVal)
        dispatch(test_page({ platform, accuracy: filter_val_show.defaultVals.accuracySetVal, start_date, end_date }))
        dispatch(test_filter({...filter_value, accuracy: filter_val_show.accuracy}))
      }

      if (checkPlateformVal && checkAccuracyVal) {
        dispatch(test_page({ platform, accuracy, start_date, end_date }))
        dispatch(test_filter(filter_value))
      }

    } else {
      dispatch(test_page({platform: filter_val_show.defaultVals.platformSetVal, accuracy: filter_val_show.defaultVals.accuracySetVal, start_date, end_date}))
      dispatch(test_filter({...filter_val_show, start_date, end_date}))
    }

    setBasicModal(!basicModal)
  }

  const refreshPage = () => {
    filter_form()
    setBasicModal(false)
  }

  useEffect(() => {

    setStartDatePicker([new Date(filter_val_show.start_date)])
    setEndDatePicker([new Date(filter_val_show.end_date)])

  }, [filter_val_show])

  if (loadding === true) {
    return <div style={{ backgroundColor: "rgb(0 0 0 / 37%)", position: "absolute", width: "100%", height: "100%", zIndex: 99999, paddingTop: "30rem" }} className="d-flex justify-content-center">
      <Spinner animation="border" type='grow' color='primary'  />
    </div>
  }

  return (
    <div className='content-header row'>
      <div className='content-header-left col-md-2 col-12 mb-2'>
        <div className='row breadcrumbs-top'>
          <div className='col-12'>
            {breadCrumbTitle ? <h4>{breadCrumbTitle}</h4> : ''}
          </div>
        </div>
      </div>

      <div className='content-header-right text-md-right col-md-10 col-12 d-md-block d-none'>
        <div className='form-group breadcrum-right dropdown'>
          <div className="d-inline-block text-primary">
            <Badge color='light-danger'>{t('Platform')}</Badge><ChevronsRight /><MultipleBadge color="danger" filterData={filter_val_show.platform} /> | <Badge color='light-primary'>{t('Accuracy')}</Badge><ChevronsRight /><Badge color='primary'>{filter_val_show.accuracy}</Badge> | <Badge color='light-success'>{t('Start Date')} </Badge> <ChevronsRight /> <Badge color='dark'>{filter_val_show.start_date}</Badge> | <Badge color='light-success'>{t('End Date')}</Badge> <ChevronsRight /> <Badge color='dark'>{filter_val_show.end_date}</Badge>
          </div>
          <Button.Ripple size='sm' color='primary' onClick={() => setBasicModal(!basicModal)} className='ml-1'>
            {t('Filter')}
          </Button.Ripple>
          <Button.Ripple size='sm' color='primary' className='ml-1' outline onClick={refreshPage}>
            <span className='align-middle mr-25'>
              {t('Refresh')}
            </span>
            <RefreshCw size={14} />
          </Button.Ripple>
          <Modal isOpen={basicModal} toggle={() => setBasicModal(!basicModal)} modalClassName="modal-primary">
            <ModalHeader toggle={() => setBasicModal(!basicModal)}>{t('Filter')}</ModalHeader>
            <ModalBody>
              <Row>
                <Col sm='12'>
                  <FormGroup>
                    <Label for="platform">{t('Platform')}</Label>
                    <Select
                      isMulti
                      id="platform"
                      isClearable={true}
                      onChange={platformHandle}
                      theme={selectThemeColors}
                      options={multiOptions.platform}
                      className='react-select'
                      classNamePrefix='select'
                      defaultValue={filter_val_show.defaultVals.platformVal}
                    />
                    {platformValid ? <Label for="platform" className="text-danger">Field cannot be blank</Label> : ""}
                  </FormGroup>
                </Col>
                <Col sm='12' md="12">
                  <FormGroup>
                    <Label for="accuracy">{t('Accuracy')}</Label>
                    <Select
                      id="accuracy"
                      onChange={accuracyHandle}
                      isClearable={true}
                      theme={selectThemeColors}
                      options={multiOptions.accuracy}
                      className='react-select'
                      classNamePrefix='select'
                      defaultValue={filter_val_show.defaultVals.accuracyVal}
                    />
                    {accuracyValid ? <Label for="accuracy" className="text-danger">Field cannot be blank</Label> : ""}
                  </FormGroup>
                </Col>                
                <Col sm='6' md="6">
                  <FormGroup>
                    <Label for='range-picker-start'>{t('Start Date')}</Label>
                    <Flatpickr
                      value={startDatePicker}
                      id='range-picker-start'
                      className='form-control'
                      onChange={date => setStartDatePicker(date)}
                      options={{
                        mode: "single",
                        allowInput: false,
                        dateFormat: "Y-m-d",
                        disable: [
                          {
                            from: addDays(new Date(), +0),
                            to: "9999-01-01"
                          }
                        ]
                      }}
                      autocomplete="off"
                      style={{ background: "white", color: "black" }}
                    />
                    {startDateValid ? <Label for="platform" className="text-danger">Field cannot be blank</Label> : ""}

                  </FormGroup>
                </Col>
                <Col sm='6' md="6">
                  <FormGroup>
                    <Label for='range-picker-end'>{t('End Date')}</Label>
                    <Flatpickr
                      value={endDatePicker}
                      id='range-picker-end'
                      className='form-control'
                      onChange={date => setEndDatePicker(date)}
                      options={{
                        mode: "single",
                        allowInput: false,
                        dateFormat: "Y-m-d",
                        disable: [
                          {
                            from: addDays(new Date(), +0),
                            to: "9999-01-01"
                          }
                        ]
                      }}
                      autocomplete="off"
                      style={{ background: "white", color: "black" }}
                    />
                    {endDateValid ? <Label for="platform" className="text-danger">Field cannot be blank</Label> : ""}
                  </FormGroup>
                </Col>
              </Row>
            </ModalBody>
            <ModalFooter>
              <div style={{ float: 'right' }}>
              <Button size="small" color="danger" onClick={() => setBasicModal(!basicModal)} >
                  {t('Close')}
                </Button>
                <Button size="small" color="primary" className="ml-1" onClick={filter_form} >
                {t('Submit')}
                </Button>
              </div>
            </ModalFooter>
          </Modal>
        </div>
      </div>
    </div>
  )
}
export default BreadCrumbs

BreadCrumbs.propTypes = {
  breadCrumbTitle: Proptypes.string.isRequired
}