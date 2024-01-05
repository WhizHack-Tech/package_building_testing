import { Link } from 'react-router-dom'
import { Sunrise, Info } from 'react-feather'
import { useTranslation } from 'react-i18next'
import { Card, CardHeader, CardTitle, CardBody, Row, Popover, PopoverHeader, PopoverBody, Badge } from 'reactstrap'
import { useState } from 'react'
import StatsVertical from '@components/widgets/stats/External'
// import StatsVertical from '@components/widgets/stats/StatsVertical'
import { useSelector } from 'react-redux'
const StatsCard = () => {
  const {t} = useTranslation()
  const [popoverOpen, setPopoverOpen] = useState(false)
  const test_page_data = useSelector((store) => store.test_page.charts)
  const chart_length = Object.keys(test_page_data).length
  return (
    <Card className='card-statistics'>
      <CardBody>
        <StatsVertical icon={<Sunrise size={21} />} color='warning' stats={(chart_length > 0) ? test_page_data.ExternalAttackCount : ""} statTitle={t('External Attack Events')} />
      </CardBody>
    </Card>
  )
}

export default StatsCard
