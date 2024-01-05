// ================================================================================================
//  File Name:  data.js
//  Description: Details of the data table.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** Custom Components
import { Fragment, useState } from 'react'
import { format } from 'date-fns'
import { useTranslation } from 'react-i18next'
// ** Third Party Components
import { ChevronDown, ChevronRight } from 'react-feather'
import { Badge, Row, TabContent, TabPane, Nav, NavItem, NavLink, Collapse, CardHeader, CardTitle, CardBody, Col } from 'reactstrap'

// ** Expandable table component
const ExpandableTable = ({ data }) => {

  const { t } = useTranslation()
  const [active, setActive] = useState('1')
const [isOpen, setIsOpen] = useState(true)
const [Isopen, setIsopen] = useState(true)
const [isOpen1, setIsOpen1] = useState(true)
  const ObjKeys = Object.keys(data)
  const ObjVal = Object.values(data)

  const ListTableData = () => {
    
    if (ObjKeys.length > 0) {
      return ObjKeys.map((values, i) => {
        return (
          <Row className="m-1" key={i}>
            <Badge color='light-primary'>
            <Col xs={4} md={4}>{values}</Col>
            </Badge>
            &nbsp;&nbsp;:
            <Col xs={8} md={4}>{JSON.stringify(ObjVal[i])}</Col>
          </Row> 
        )
      })

    } else {
      return <p>{t('Data Not Found')}</p>
    }

  }

  const JsonRenderData = () => {
    
    if (ObjKeys.length > 0) {
      return <pre style={{color:"#8177f2"}}> {JSON.stringify(data, null, '\t')} </pre>
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
        <NavItem>
          <NavLink
            active={active === '3'}
            onClick={() => {
              toggle('3')
            }}
          >
            {t('Rule')}
          </NavLink>
        </NavItem>
      </Nav>
      <TabContent className='py-50 ml-1' activeTab={active}>
        <TabPane tabId='1'>
          <ListTableData />
        </TabPane>
        <TabPane tabId='2'>
         <JsonRenderData/>
        </TabPane>
        <TabPane tabId='3'>
          <div>
            <CardHeader>
              <CardTitle tag='h4' onClick={() => { setIsOpen(!isOpen) }}> <div className='views cursor-pointer d-inline-block pr-1'>
                {isOpen ? <ChevronDown size='18' /> : <ChevronRight size='18' />}
              </div>
                {t('Information')}</CardTitle>
              
            </CardHeader>
            <Collapse isOpen={isOpen}>
              <hr />
              <CardBody>
                <Row>
                  <Col xs={1} md={3}> {('ID')} : <Badge color='primary'>{data.rule_id}</Badge></Col>
                  <Col xs={1} md={3}> {t('Level')} : <Badge color='secondary'>{data.rule_level}</Badge></Col>
                  <Col xs={1} md={5}> {t('Groups')} : <Badge color='warning'>{data.rule_}</Badge></Col>
                </Row>
              </CardBody>
            </Collapse>
            <hr />
          </div>
          <div>
            <CardHeader>
              <CardTitle tag='h4' onClick={() => { setIsopen(!Isopen) }}> <div className='views cursor-pointer d-inline-block pr-1'>
                {Isopen ? <ChevronDown size='18' /> : <ChevronRight size='18' />}
              </div>
                {t('Details')}</CardTitle>
              
            </CardHeader>
            <Collapse isOpen={Isopen}>
              <hr />
              <CardBody>
                <Row >
                  <Col xs={1} md={3}> {t('Category')} : <Badge color='light-primary'>{data.decoder_name}</Badge></Col>
                  <Col xs={1} md={6}> {t('System Event ID')} : <Badge color='light-warning'>{data.data_win_system_eventID}</Badge></Col>
                </Row>
              </CardBody>
            </Collapse>
            <hr />
          </div>
          <div>
            <CardHeader>
              <CardTitle tag='h4' onClick={() => { setIsOpen1(!isOpen1) }}> <div className='views cursor-pointer d-inline-block pr-1'>
                {isOpen1 ? <ChevronDown size='18' /> : <ChevronRight size='18' />}
              </div>
                {t('Compliance')}</CardTitle>
              
            </CardHeader>
            <Collapse isOpen={isOpen1}>
              <hr />
              <CardBody>
                <Row >
                  <Col xs={1} md={3}> {t('GDPR')} : <Badge color='light-primary'>{data.rule_gdpr}</Badge></Col>
                  <Col xs={1} md={3}> {t('GPG 13')} : <Badge color='light-warning'>{data.rule_gpg13}</Badge></Col>
                  <Col xs={1} md={3}> {t('HIPAA')} : <Badge color='light-success'>{data.rule_hipaa}</Badge></Col>
                  <Col xs={1} md={3}> {t('MITRE')} : <Badge color='info'>{data.rule_mitre_id}</Badge></Col>
                </Row>
              </CardBody>
            </Collapse>
            <hr />
          </div>
        </TabPane>
      </TabContent>
      </div>
    </Fragment>
  )
}

// ** Table Common Column
export const Columns = () => {
  const { t } = useTranslation()
  return [
  {
    name: t('Timestamp'),
    selector: 'timestamp',
    sortable: true,
    minWidth: '150px',
    cell: row => {
      return (
        <div className='d-flex justify-content-left align-items-center'>
          <Badge color='light-primary'>
            <span className='font-weight-bold text-uppercase'>{format(new Date(row.timestamp), "yyyy-MM-dd, h:mm:ss a")}</span>
          </Badge>
        </div>
      )
    }
  },
  {
    name: t('Technique(s)'),
    selector: 'rule_gdpr',
    sortable: true,
    minWidth: '100px',
    cell: row => {
        return (
          <div>
            <Badge color='info'>{row.rule_gdpr}</Badge>
          </div>
        )
      }
  },
  {
    name: t('Tactics'),
    selector: 'rule_mitre_tactic',
    sortable: true,
    minWidth: '100px',
    cell: row => {
        return (
          <div>
            <Badge color='warning'>{row.rule_mitre_tactic}</Badge>
          </div>
        )
      }
  },
  {
    name: t('Description'),
    selector: 'rule_description',
    sortable: true,
    minWidth: '250px'
  },
  {
    name: t('Level'),
    selector: 'rule_level',
    sortable: true,
    minWidth: '100px',
    cell: row => {
        return (
          <div>
            <Badge color='danger'>{row.rule_mitre_tactic}</Badge>
          </div>
        )
      }
  },
  {
    name: t('Rule ID'),
    selector: 'rule_id',
    sortable: true,
    minWidth: '150px',
    cell: row => {
        return (
          <div>
            <Badge color='secondary'>{row.rule_id}</Badge>
          </div>
        )
      }
  }

]
}

export default ExpandableTable
