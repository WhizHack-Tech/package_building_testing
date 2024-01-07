    // Filename : Lateral.js
    // Purpose/Description : This page is calculating the data of total number of critical Internal attacks in the enviroment 
    // Author : Jaydeep Roy Sarkar (EMP-0020), Danish Ansari (EMP-0037) and Sai Kaladhar (EMP-0017)
    // Copyright (c) : Whizhack Technologies (P) Ltd.

import { Link } from 'react-router-dom'
import { Sunrise, Info } from 'react-feather'
import { Card, CardHeader, CardBody, CardTitle, Row, Popover, PopoverHeader, PopoverBody, Badge } from 'reactstrap'
import { useState } from 'react'
import StatsVertical from '@components/widgets/stats/Internal'
import { useSelector } from 'react-redux'
import { useTranslation } from 'react-i18next'
const StatsCard = () => {
  const {t} = useTranslation()
  const [popoverOpen, setPopoverOpen] = useState(false)
  const dashboard_charts_data = useSelector((store) => store.dashboard_charts.charts)
  const chart_length = Object.keys(dashboard_charts_data).length
  return (
    <Card className='card-statistics'>
      <CardHeader>
        <CardTitle tag='h4'>{t('Internal Attacks')}</CardTitle>
        <Badge color='primary'>
          <Link><Info id='Lateral_Movement_Attack_Count' size={20} /></Link>
        </Badge>
        <Popover
          placement='top'
          target='Lateral_Movement_Attack_Count'
          isOpen={popoverOpen}
          toggle={() => setPopoverOpen(!popoverOpen)}
        >
          <PopoverHeader>{t('Internal Attacks')}</PopoverHeader>
          <PopoverBody>
          {t('Total number of critical Internal attacks')}
          </PopoverBody>
        </Popover>
      </CardHeader>
      <CardBody>
        <StatsVertical  stats={(chart_length > 0) ? dashboard_charts_data.lateral_attack_count : ""} statTitle={t('Lateral Movement Attacks')} />
      </CardBody>
    </Card>
  )
}

export default StatsCard
