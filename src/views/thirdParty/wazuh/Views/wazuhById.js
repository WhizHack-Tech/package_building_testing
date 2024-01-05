import { addDays, format } from "date-fns"
import { Fragment, useState, useEffect, useMemo } from 'react'
import { Redirect, useParams } from "react-router-dom"
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
import Topactics from './Toptactics'
import Alertslinechart from './Alertslinechart'
import Mitreattacks from './Mitreattcks'
// axios import
import axios from '@axios'

const WazuhById = () => {
  const { t } = useTranslation()
  const [activeTab, setActiveTab] = useState('1')
  const [basicModal, setBasicModal] = useState(false)
  const [startDate, setStartDate] = useState(addDays(new Date(), -3))
  const [endDate, setEndDate] = useState(new Date())
  const [filterDateStart, setFilterDateStart] = useState(format(new Date(), "yyyy-MM-dd"))
  const [filterDateEnd, setFilterDateEnd] = useState(format(new Date(), "yyyy-MM-dd"))
  const { id } = useParams()
  const [loadding, setLoadding] = useState(false)
  //Data bind for components child #START.
  const [top5Alert, setTop5Alert] = useState([])
  const [top5rule, setTop5rule] = useState([])
  const [security_event, setSecurity_event] = useState([])
  const [top5pic, setTop5pic] = useState([])
  const [toptactics, setToptactics] = useState([])
  const [rule_attack, setRule_attack] = useState([])
  const [rule_tactics, setRule_tactics] = useState([])
  const [alerts_evolution, setAlerts_evolution] = useState([])
  const [alert_Groups, setAlert_Groups] = useState([])
  const [mitre_Attacks, setMitre_Attacks] = useState([])
  //Data bind for components child #END.

  const toggleTab = tab => {
    setActiveTab(tab)
  }

  const filterHandle = () => {
    let start_date = new Date()
    let end_date = new Date()
    setLoadding(true)
    if (startDate.length > 0 && startDate[0] !== "") {
      start_date = format(startDate[0], "yyyy-MM-dd")
    } else {
      start_date = format(addDays(new Date(), -3), "yyyy-MM-dd")
    }

    if (endDate.length > 0 && endDate[0] !== "") {
      end_date = format(endDate[0], "yyyy-MM-dd")
    } else {
      end_date = format(end_date, "yyyy-MM-dd")
    }

    setFilterDateEnd(end_date)
    setFilterDateStart(start_date)

    axios.post(`wazuh-queries-security-event-page`, {
      start_date,
      end_date,
      agent_id: id
    }, { headers: { Authorization: token() } })
    .then(res => {

      setLoadding(false)

      if (res.data.top_five_alert.message_type === "data_found") {
        setTop5Alert(res.data.top_five_alert.data)
      }

      if (res.data.top_five_rule_groups.message_type === "data_found") {
        setTop5rule(res.data.top_five_rule_groups.data)
      }

      if (res.data.security_alerts.message_type === "data_found") {
        setSecurity_event(res.data.security_alerts.data)
      }
      if (res.data.top_five_pci_dss_requirements.message_type === "data_found") {
        setTop5pic(res.data.top_five_pci_dss_requirements.data)
      }
      if (res.data.top_tactics.message_type === "data_found") {
        setToptactics(res.data.top_tactics.data)
      }

      if (res.data.rule_level_by_attack.message_type === "data_found") {
        setRule_attack(res.data.rule_level_by_attack.data)
      }

      if (res.data.rule_level_by_tactics.message_type === "data_found") {
        setRule_tactics(res.data.rule_level_by_tactics.data)
      }

      if (res.data.alerts_evolution_over_time.message_type === "data_found") {
        setAlerts_evolution(res.data.alerts_evolution_over_time.data)
      }

      if (res.data.alert_groups_evolution_security.message_type === "data_found") {
        setAlert_Groups(res.data.alert_groups_evolution_security.data)
      }
      if (res.data.mitre_attack_by_tactic.message_type === "data_found") {
        setMitre_Attacks(res.data.mitre_attack_by_tactic.data)
      }
     

    }).catch(errors => {
      setLoadding(false)
    })
  }

  useEffect(() => {
    filterHandle()
  }, [])

  return (
    <Fragment>
      {(loadding === true) ? <div style={{ backgroundColor: "rgb(0 0 0 / 37%)", position: "absolute", width: "100%", height: "100%", zIndex: 99999, paddingTop: "30rem" }} className="d-flex justify-content-center">
        <Spinner animation="border" type='grow' color='primary' />
      </div> : null}
      <div className='content-header row'>
        <div className='content-header-left col-md-4 col-12'>
          <div className='row breadcrumbs-top'>
            <div className='col-12'>
              <Tabs activeTab={activeTab} toggleTab={toggleTab} />
            </div>
          </div>
        </div>
        <div className='content-header-right text-md-right col-md-8 col-12 d-md-block d-none'>
          <div className='form-group breadcrum-right dropdown'>
            <div className="d-inline-block text-primary">
              <Badge color='light-success'>{t('Start Date')}</Badge> <ChevronsRight /> <Badge color='dark'>{filterDateStart}</Badge> | <Badge color='light-success'>{t('End Date')}</Badge> <ChevronsRight /> <Badge color='dark'>{filterDateEnd}</Badge>
            </div>
            <Button.Ripple color='primary' size='sm' onClick={() => setBasicModal(!basicModal)} className='ml-1'>
              {t('Filter')}
            </Button.Ripple>
            <Button.Ripple size='sm' color='primary' className='ml-1' outline onClick={filterHandle}>
            <span className='align-middle mr-25'>
              {t('Refresh')}
            </span>
            <RefreshCw size={14} />
          </Button.Ripple>
            <Modal isOpen={basicModal} toggle={() => setBasicModal(!basicModal)} modalClassName="modal-primary">
              <ModalHeader toggle={() => setBasicModal(!basicModal)}>{t('Filter')}</ModalHeader>
              <ModalBody>
                <Row>
                  <Col sm='6' md="6">
                    <FormGroup>
                      <Label for='range-picker-start'>{t('Start Date')}</Label>
                      <Flatpickr
                        id='range-picker-start'
                        className='form-control'
                        value={startDate}
                        onChange={date => { setStartDate(date) }}
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
                    </FormGroup>
                  </Col>
                  <Col sm='6' md="6">
                    <FormGroup>
                      <Label for='range-picker-end'>{t('End Date')}</Label>
                      <Flatpickr
                        id='range-picker-end'
                        className='form-control'
                        value={endDate}
                        onChange={date => { setEndDate(date) }}
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
                    </FormGroup>
                  </Col>
                </Row>
              </ModalBody>
              <ModalFooter>
                <div style={{ float: 'right' }}>
                  <Button size="small" color="danger" onClick={() => setBasicModal(!basicModal)} >
                    {t('Close')}
                  </Button>
                  <Button size="small" color="primary" className="ml-1" onClick={() => {
                    filterHandle()
                    setBasicModal(false)
                  }}>
                    {t('Submit')}
                  </Button>
                </div>
              </ModalFooter>
            </Modal>
          </div>
        </div>
      </div>
      <TabContent activeTab={activeTab}>
        <TabPane tabId='1'>
          {/* <Row>
            <Col>
              <Details agent_details={agent_details}/>
            </Col>
          </Row> */}
          <Row className='match-height'>
            <Col lg='4' md='12' xs='12'>
              <Top5alerts top5Alert={top5Alert} />
            </Col>
            <Col lg='4' md='12' xs='12'>
              <Toprulegroups top5rule={top5rule} />
            </Col>
            <Col lg='4' md='12' xs='12'>
              <Top5pcidss top5pic={top5pic}/>
            </Col>
          </Row>
          <Row>
            <Col sm='12'>
              <Linechart alert_Groups={alert_Groups}/>
            </Col>
          </Row>
          <Row>
            <Col sm='12'>
              <TableExpandable security_event={security_event} />
            </Col>
          </Row>
        </TabPane>

        <TabPane tabId='2'>
          <Row className='match-height'>
            <Col sm='8'>
              <Alertslinechart alerts_evolution={alerts_evolution} />
            </Col>
            <Col lg='4' md='12' xs='12'>
              <Topactics toptactics={toptactics} />
            </Col>
          </Row>
          <Row className='match-height'>
            <Col lg='4' md='12' xs='12'>
              <RuleAttack rule_attack={rule_attack} />
            </Col>
            <Col sm='4'>
              <Mitreattacks mitre_Attacks={mitre_Attacks}/>
            </Col>
            <Col lg='4' md='12' xs='12'>
              <Rulelevel rule_tactics={rule_tactics} />
            </Col>
          </Row>
        </TabPane>
      </TabContent>
    </Fragment>
  ) 
}

export default WazuhById