    // Filename : Severity1.js
    // Purpose/Description : In this page we are calculating the number of attached made in the enviroment total count based on the filteration 
    // Author : Jaydeep Roy Sarkar (EMP-0020), Danish Ansari (EMP-0037) and Sai Kaladhar (EMP-0017)
    // Copyright (c) : Whizhack Technologies (P) Ltd.
// Importing Component from verial folders of the project
import { Link } from 'react-router-dom'
import { TrendingUp, User, Box, Info, Sunset, AlertOctagon, MessageSquare } from 'react-feather'
import { Card, CardHeader, CardTitle, CardBody, CardText, Row, Col, Media, Button, Popover, PopoverHeader, PopoverBody, Badge } from 'reactstrap'
import { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
// import Critical from "../../../assets/images/svg/Critical.svg"
//import react-intl library for language change
// import { FormattedMessage } from 'react-intl'
import { useTranslation } from 'react-i18next'
import StatsVertical from '@components/widgets/stats/StatsVertical'
const StatsCard = () => {
  const {t} = useTranslation()
  const [popoverOpen, setPopoverOpen] = useState(false)
  const dashboard_charts_data = useSelector((store) => store.dashboard_charts.charts)
  const chart_length = Object.keys(dashboard_charts_data).length
  return (
    <Card className='card-statistics'>
      <CardHeader>
        <CardTitle tag='h4'>{t('Critical Threats')}</CardTitle>
        <Badge color='primary'>
          {/* <Link>
          <Info id='Most_Threat_Attacks' size={20} />
          </Link> */}
          <Link><Info id='Most_Threat_Attacks' size={20} /></Link>
        </Badge>
        <Popover
          placement='top'
          target='Most_Threat_Attacks'
          isOpen={popoverOpen}
          toggle={() => setPopoverOpen(!popoverOpen)}
        >
          <PopoverHeader>{t('Critical Threats')}</PopoverHeader>
          <PopoverBody>
          {t('Total number of critical Internal and External attacks')}
          </PopoverBody>
        </Popover>
      </CardHeader>
      <CardBody>
        <StatsVertical stats={(chart_length > 0) ? dashboard_charts_data.severity1_attack_count : ""} statTitle= {t('High Severity Events')} />
      </CardBody>
    </Card>
  )
}

export default StatsCard
