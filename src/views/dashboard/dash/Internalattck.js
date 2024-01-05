    // Filename : Internalattack.js
    // Purpose/Description : This page is calculating the data of total number of compromised hosts in the enviroment based on the filter 
    // Author : Jaydeep Roy Sarkar (EMP-0020), Danish Ansari (EMP-0037) and Sai Kaladhar (EMP-0017)
    // Copyright (c) : Whizhack Technologies (P) Ltd.
import { Link } from 'react-router-dom'
import { TrendingUp, User, Box, Info, Sunset, MessageSquare } from 'react-feather'
import { Card, CardHeader, CardTitle, CardBody, CardText, Row, Col, Media, Button, Popover, PopoverHeader, PopoverBody, Badge } from 'reactstrap'

import { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { FormattedMessage } from 'react-intl'
import { useTranslation } from 'react-i18next'
// import Botnet from "../../../assets/images/svg/Botnet.svg"
import StatsVertical from '@components/widgets/stats/Botnet'
const StatsCard = ({ cols }) => {
  const {t} = useTranslation()
  const [popoverOpen, setPopoverOpen] = useState(false)
  const dashboard_charts_data = useSelector((store) => store.dashboard_charts.charts)
  const chart_length = Object.keys(dashboard_charts_data).length
  return (
    <Card className='card-statistics'>
      <CardHeader>
        <CardTitle tag='h4'>{t('Outgoing Botnet Connections')}</CardTitle>
        <Badge color='primary'>
          <Link><Info id='Internal_Attack_Count' size={20} /></Link>
        </Badge>
        <Popover
          placement='top'
          target='Internal_Attack_Count'
          isOpen={popoverOpen}
          toggle={() => setPopoverOpen(!popoverOpen)}
        >
          <PopoverHeader>{t('Outgoing Botnet Connections')}</PopoverHeader>
          <PopoverBody>
          {t('Total Number of Compromised Hosts')}
          </PopoverBody>
        </Popover>
      </CardHeader>
      <CardBody>
        <StatsVertical stats={(chart_length > 0) ? dashboard_charts_data.internalCompromised_attack_count : ""} statTitle={t('Internal Attack Count')} />
      </CardBody>
    </Card>
  )
}

export default StatsCard
