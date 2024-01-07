// ================================================================================================
//  File Name: wazuhById.js
//  Description: Details of the HIDS Incident Graph.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { addDays, format } from "date-fns"
import { Fragment, useState, useEffect, useMemo } from 'react'
// import { useLocation } from 'react-router-dom'
import { useLocation, useParams } from "react-router-dom"
import { useTranslation } from 'react-i18next'
import Flatpickr from 'react-flatpickr'
import { ChevronsRight, RefreshCw } from 'react-feather'
import {
  Button,
  Spinner,
  TabPane,
  TabContent,
  Badge,
  Label,
  Row,
  Col,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  FormGroup
} from 'reactstrap'
import { token } from '@utils'
import '@styles/react/libs/tables/react-dataTable-component.scss'
import '@styles/react/libs/flatpickr/flatpickr.scss'
import '@styles/react/libs/charts/apex-charts.scss'
import '@styles/react/libs/maps/map-leaflet.scss'
import Tabs from './Tabs'
import loaderSrc from "@assets/images/logo/hids.gif"
// ** Tables
import TableExpandable from './TableExpandable'
// ** charts
import Top5alerts from './Top5alerts'
import Top5pcidss from './Top5pcidss'
import Toprulegroups from './Top5rulegroups'
import Linechart from './Linechart'
// import Details from './Details'
import Rulelevel from './Rulelevel'
import RuleAttack from './Ruleattack'
// import Topactics from './Toptactics'
import Alertslinechart from './Alertslinechart'
import Mitreattacks from './Mitreattcks'
// axios import
import axios from '@axios'

const WazuhById = () => {
  const { t } = useTranslation()
  const { search } = useLocation()
  const searchParams = useMemo(() => new URLSearchParams(search), [search])
  const [activeTab, setActiveTab] = useState('1')

  const toggleTab = tab => {
    setActiveTab(tab)
  }


  return (
    <Fragment>
      <Tabs activeTab={activeTab} toggleTab={toggleTab} />
      <TabContent activeTab={activeTab}>
        <TabPane tabId='1'>
          <Row className='match-height'>
            <Col lg='4' md='12' xs='12'>
              <Top5alerts />
            </Col>
            <Col lg='4' md='12' xs='12'>
              <Toprulegroups />
            </Col>
            <Col lg='4' md='12' xs='12'>
              <Top5pcidss />
            </Col>
          </Row>
          <Row>
            <Col sm='12'>
              <Linechart />
            </Col>
          </Row>
          <Row>
            <Col sm='12'>
              <TableExpandable />
            </Col>
          </Row>
        </TabPane>

        <TabPane tabId='2'>
          <Row className='match-height'>
            <Col sm='8'>
              <Alertslinechart />
            </Col>
            <Col lg='4' md='12' xs='12'>
              <RuleAttack />
            </Col>
            {/* <Col lg='4' md='12' xs='12'>
              <Topactics toptactics={toptactics} />
            </Col> */}
          </Row>
          <Row className='match-height'>
            <Col lg='4' md='12' xs='12'>
              <Rulelevel />
            </Col>
            <Col sm='8'>
              <Mitreattacks />
            </Col>
          </Row>
        </TabPane>
      </TabContent>
    </Fragment>
  ) 
}

export default WazuhById