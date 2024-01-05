    // Filename : External.js
    // Purpose/Description : This page is calculating the data of total number of critical External attacks 
    // Author : Jaydeep Roy Sarkar (EMP-0020), Danish Ansari (EMP-0037) and Sai Kaladhar (EMP-0017)
    // Copyright (c) : Whizhack Technologies (P) Ltd.
import { Link } from 'react-router-dom'
import { Sunrise, Info } from 'react-feather'
// import { FormattedMessage } from 'react-intl'
import { useTranslation } from 'react-i18next'
import { Card, CardHeader, CardTitle, CardBody, Row, Popover, PopoverHeader, PopoverBody, Badge } from 'reactstrap'
import { useState } from 'react'
import StatsVertical from '@components/widgets/stats/External'
import { useSelector } from 'react-redux'
// import external from "../../../assets/images/svg/external.svg"
const StatsCard = () => {
  const {t} = useTranslation()
  const [popoverOpen, setPopoverOpen] = useState(false)
  const dashboard_charts_data = useSelector((store) => store.dashboard_charts.charts)
  const chart_length = Object.keys(dashboard_charts_data).length
  return (
    <Card className='card-statistics'>
      <CardHeader>
        <CardTitle tag='h4'>{t('External Attacks')}</CardTitle>
        <Badge color='primary'>
          <Link><Info id='External_Attack_Count' size={20} /></Link>
        </Badge>
        <Popover
          placement='top'
          target='External_Attack_Count'
          isOpen={popoverOpen}
          toggle={() => setPopoverOpen(!popoverOpen)}
        >
          <PopoverHeader>{t('External Attacks')}</PopoverHeader>
          <PopoverBody>
          {t('Total number of critical External attacks')}
          </PopoverBody>
        </Popover>
      </CardHeader>
      <CardBody>
        <StatsVertical stats={(chart_length > 0) ? dashboard_charts_data.external_attack_count : ""} statTitle={t('Attack Events')} />
      </CardBody>
    </Card>
  )
}

export default StatsCard
