// ==============================================================================================
//  File Name: globol_therats.js
//  Description: Details of the globol threats chart component.
// ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** React Imports
import { useState } from "react"
import "./hover.css"

// ** Third Party Components
import Proptypes from "prop-types"
import "react-date-range/dist/styles.css" // main style file
import "react-date-range/dist/theme/default.css" // theme css file
import OptionsRepead from "@components/repeater/option"
// ** Reactstrap Imports
import { Col, Row, CardTitle, InputGroup, Input, InputGroupText, Collapse, CardBody, Card, Button, Form } from "reactstrap"
import { toast } from 'react-toastify'

import { Calendar, ChevronDown, ChevronRight } from 'react-feather'
import { useDispatch, useSelector } from "react-redux"
// import { filterValues } from '../../../views/nids/store/dashboard_chart'
import { filterValues } from '../../../views/trace/global_threat_feed/store/global_charts'
import { useTranslation } from 'react-i18next'
let setIntervalFun = null
const BreadCrumbs = props => {
  const { t } = useTranslation()
  const { breadCrumbTitle } = props
  const [isOpen, setIsOpen] = useState(false)
  const [filters, setFilters] = useState({ name: t('Last 1 hour'), value: 'last_24_hours' })
  const [reloadVal, setReloadVal] = useState('off')
  const [timeVal, setTimeVal] = useState(1)

  const dispatch = useDispatch()
  const filterStore = useSelector((state => state.global_charts))

  function funFilters({ name, value }) {
    setFilters({ name, value })
    dispatch(filterValues({ filters: value, filter_name: name, refreshCount: 1 }))
    setIsOpen(false)
  }

  const applyReload = () => {
    let interval = 60000

    if (reloadVal === 'minute') {
      clearInterval(setIntervalFun)
      interval = 60000 * parseInt(timeVal)
    } else if (reloadVal === 'hour') {
      clearInterval(setIntervalFun)
      interval = 3600000 * parseInt(timeVal)
    }

    if (reloadVal !== 'off') {
      let refreshCount = 1

      toast.success(`The page will refresh every ${timeVal} ${reloadVal}.`, {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined
      })

      setIntervalFun = setInterval(() => {
        
        dispatch(filterValues({ filters: filters.value, filter_name: filters.name, refreshCount }))
        refreshCount++
      }, interval)
    } else {
      clearInterval(setIntervalFun)
      setIntervalFun = null

      toast.success(`Refresh has been off.`, {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined
      })
    }
    setIsOpen(false)
  }

  return (
    <div className='content-header row'>
      <div className='content-header-left col-md-8 col-12 mb-1'>
        <div className='row breadcrumbs-top'>
          <div className='col-12'>
            {breadCrumbTitle ? <h4>{breadCrumbTitle}</h4> : ''}
          </div>
        </div>
      </div>
      <div className="content-header-left col-md-4 col-12 d-md-block d-none">
        <div className="breadcrumb-left dropdown">
          <Form>
            <InputGroup className='mb-2'>
              <InputGroupText onClick={() => { setIsOpen(!isOpen) }}>
                <Calendar size={14} />
                &nbsp;&nbsp;
                {isOpen ? <ChevronDown size='18' /> : <ChevronRight size='18' />}
              </InputGroupText>
              {/* <Input value={filters.name || ''} placeholder= {t('Last 24 Hours')} name="filter_name" onChange={(e) => setFilters({ ...filters, name: e.target.value })} /> */}
              <Input value={filterStore.filter_name || filters.name} placeholder= {t("Last 1 hour")} name="filter_name" onChange={(e) => setFilters({ ...filters, name: e.target.value })} />
              {/* <Input defaultValue={filters.name} placeholder='Today' name="filter_name" /> */}
            </InputGroup>
            <Collapse isOpen={isOpen} style={{ position: 'fixed', zIndex: 1 }}>
              <Card>
                <CardBody>
                  <CardTitle tag='h4'>Commonly Used</CardTitle>
                  <Row>
                    <Col sm='6'>
                      <span className='join' onClick={() => funFilters({ name: t('Last 5 minutes'), value: "last_24_hours" })} >{t('Last 5 minutes')}</span>
                      {/* <span className="collapse-close" onClick={() => setIsOpen(false)}>&times;</span> */}
                    </Col>
                    <Col>
                      <span className='join' onClick={() => funFilters({ name: t("Last 6 Hours"), value: "last_24_hours" })}>{t('Last 6 Hours')}</span>
                    </Col>
                  </Row>
                  <Row>
                    <Col>
                      <span className='join' onClick={() => funFilters({ name: t('Last 15 minutes'), value: "last_24_hours" })}>{t('Last 15 minutes')}</span>
                    </Col>
                    <Col>
                      <span className='join' onClick={() => funFilters({ name: t("Last 12 Hours"), value: "last_24_hours" })}>{t('Last 12 Hours')}</span>
                    </Col>
                  </Row>
                  <Row>
                    <Col>
                      <span className='join' onClick={() => funFilters({ name: t("Last 30 minutes"), value: "last_24_hours" })}>{t('Last 30 minutes')}</span>
                    </Col>
                    <Col>
                      <span className='join' onClick={() => funFilters({ name: t("Last 24 Hours"), value: "last_24_hours" })}>{t('Last 24 Hours')}</span>
                    </Col>
                  </Row>
                  <Row>
                    <Col>
                      <span className='join' onClick={() => funFilters({ name: t("Last 1 Hour"), value: "last_24_hours" })}>{t('Last 1 hour')}</span>
                    </Col>
                    <Col>
                      <span className='join' onClick={() => funFilters({ name: t("Last 7 Days"), value: "last_7_days" })}>{t('Last 7 Days')}</span>
                    </Col>
                  </Row>
                  <Row>
                    <Col sm='12'>
                      <hr />
                      <CardTitle tag='h4'>{t('Refresh every')}</CardTitle>
                    </Col>
                    <Col sm='4' md="4">
                      <Input type='select' onChange={(e) => setTimeVal(e.target.value)}>
                        <option value='' disabled select="false">...{t('Select')}...</option>
                        <OptionsRepead options={30} />
                      </Input>
                    </Col>
                    <Col sm='5' md="5">
                      <Input type='select' onChange={(e) => setReloadVal(e.target.value)}>
                        <option value='' disabled select="false">...{t('Select')}...</option>
                        <option value='off'>{t('Off')}</option>
                        <option value='minute'>{t('Minute')}</option>
                        <option value='hour'>{t('Hour')}</option>
                      </Input>
                    </Col>
                    <Col sm='3' md="3">
                      <Button.Ripple color='primary' onClick={applyReload} type='button' outline>
                        {t('Apply')}
                      </Button.Ripple>
                    </Col>
                  </Row>
                </CardBody>
              </Card>
            </Collapse>
          </Form>
        </div>
      </div>
    </div>
  )
}
export default BreadCrumbs

// ** PropTypes
BreadCrumbs.propTypes = {
  breadCrumbTitle: Proptypes.string.isRequired
}