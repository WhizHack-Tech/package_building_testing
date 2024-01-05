    // Filename : Detectiontype.js
    // Purpose/Description : Detection type representing alert signature's count based on different type of detection mechanism (IDS/ML/DL) 
    // Author : Jaydeep Roy Sarkar (EMP-0020), Danish Ansari (EMP-0037) and Sai Kaladhar (EMP-0017)
    // Copyright (c) : Whizhack Technologies (P) Ltd.
import { Fragment, useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Avatar from '@components/avatar'
import * as Icon from 'react-feather'
// import { FormattedMessage } from 'react-intl'
import { useTranslation } from 'react-i18next'
import { Info } from 'react-feather'
import { useSelector } from "react-redux"
import { TabContent, CardHeader, CardTitle, TabPane, Nav, NavItem, NavLink, Card, CardBody, Media, Popover, PopoverHeader, PopoverBody, Badge } from 'reactstrap'
import IdsImg from "../../../assets/images/svg/ids.svg"
import MlImg from "../../../assets/images/svg/ml.svg"
import DImg from "../../../assets/images/svg/dl.svg"
const TabsJustified = () => {
  const {t} = useTranslation()
  const [popoverOpen, setPopoverOpen] = useState(false)
  const [active, setActive] = useState('1')
  const charts_data = useSelector((store) => store.dashboard_charts.charts)
  const chart_length = Object.keys(charts_data).length
  const mlData = [], idsData = [], dlData = []
  if (chart_length > 0) {

    if (charts_data.MlThreatCount.length > 0) {    
      charts_data.MlThreatCount.forEach(element => {
        mlData.push({
          title: element.name,
          color: 'light-primary',
          amount: element.val,
          Icon: <img width={30} src={MlImg} />
        }) 
      })
    }

    if (charts_data.IdsThreatCount.length > 0) {    
      charts_data.IdsThreatCount.forEach(element => {
        idsData.push({
          title: element.name,
          color: 'light-danger',
          amount: element.val,
          Icon: <img width={30} src={IdsImg} />
        }) 
      })
    }

    if (charts_data.DlThreatCount.length > 0) {    
      charts_data.DlThreatCount.forEach(element => {
        dlData.push({
          title: element.name,
          color: 'light-info',
          amount: element.val,
          Icon: <img width={30} src={DImg} />
        }) 
      })
    }
  }

  const IDS = idsData.map((item, key) => {
    return (
      <div className='transaction-item' key={key}>
        <Media className="d-flex align-items-center">
          <Avatar className='rounded' color={item.color} icon={item.Icon} />
          <Media body>
            <h6 className='transaction-title'>{item.title}</h6>
            <small>{item.subtitle}</small>
          </Media>
        </Media>
        <div className={`font-weight-bolder ${item.down ? 'text-danger' : 'text-success'}`}>{item.amount}</div>
      </div>
    )
  })

  const ML = mlData.map((item, key) => {
    return (
      <div className='transaction-item' key={key}>
        <Media className="d-flex align-items-center">
          <Avatar className='rounded' color={item.color} icon={item.Icon} />
          <Media body>
            <h6 className='transaction-title'>{item.title}</h6>
            <small>{item.subtitle}</small>
          </Media>
        </Media>
        <div className={`font-weight-bolder ${item.down ? 'text-danger' : 'text-success'}`}>{item.amount}</div>
      </div>
    )
  })

  const DL = dlData.map((item, key) => {
    return (
      <div className='transaction-item' key={key}>
        <Media className="d-flex align-items-center">
          <Avatar className='rounded' color={item.color} icon={item.Icon} />
          <Media body>
            <h6 className='transaction-title'>{item.title}</h6>
            <small>{item.subtitle}</small>
          </Media>
        </Media>
        <div className={`font-weight-bolder ${item.down ? 'text-danger' : 'text-success'}`}>{item.amount}</div>
      </div>
    )
  })


  const toggle = tab => {
    if (active !== tab) {
      setActive(tab)
    }
  }
  return (
    <Fragment>
      <Card>
        <CardHeader>
          <CardTitle tag='h4'>{t('Detected Threat Type')}</CardTitle>
          <Badge color='primary' size={20}>
            <Link><Info id='Detected_Threat_Classes' size={20} /></Link>
          </Badge>
          <Popover
            placement='top'
            target='Detected_Threat_Classes'
            isOpen={popoverOpen}
            toggle={() => setPopoverOpen(!popoverOpen)}
          >
            <PopoverHeader>{t('Detected Threat Type')}</PopoverHeader>
            <PopoverBody>
           {t('Top threat types detected by the Triple Layer Detection Engines')}
            </PopoverBody>
          </Popover>
        </CardHeader>
        <CardBody>
          <Nav tabs justified>
            <NavItem>
              <NavLink
                active={active === '1'}
                onClick={() => {
                  toggle('1')
                }}
              >
                {t('IDS')}
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink
                active={active === '2'}
                onClick={() => {
                  toggle('2')
                }}
              >
                {t('ML')}
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink
                active={active === '3'}
                onClick={() => {
                  toggle('3')
                }}
              >
                {t('DL')}
              </NavLink>
            </NavItem>
          </Nav>
          <TabContent className='py-50' activeTab={active}>
            <TabPane tabId='1'>
              <Card className='card-transaction'>
                <CardBody>{IDS}</CardBody>
              </Card>
            </TabPane>
            <TabPane tabId='2'>
              <Card className='card-transaction'>
                <CardBody>{ML}</CardBody>
              </Card>
            </TabPane>
            <TabPane tabId='3'>
              <Card className='card-transaction'>
                <CardBody>{DL}</CardBody>
              </Card>
            </TabPane>
          </TabContent>
        </CardBody>
      </Card>
    </Fragment>
  )
}
export default TabsJustified