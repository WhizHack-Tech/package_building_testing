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
  const test_page_data = useSelector((store) => store.test_page.charts)
  const chart_length = Object.keys(test_page_data).length
  return (
    <Card className='card-statistics'>
      <CardBody>
        <StatsVertical icon={<Info size={21} />} color='danger' stats={(chart_length > 0) ? test_page_data.LateralAttackCount : ""} statTitle={t('Lateral Movement Attacks')} />
      </CardBody>
    </Card>
  )
}

export default StatsCard
