import { Link } from 'react-router-dom'
import { TrendingUp, User, Box, Info, Sunset, AlertOctagon, MessageSquare } from 'react-feather'
import { Card, CardHeader, CardTitle, CardBody, CardText, Row, Col, Media, Button, Popover, PopoverHeader, PopoverBody, Badge } from 'reactstrap'
import { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useTranslation } from 'react-i18next'
import StatsVertical from '@components/widgets/stats/StatsVertical'
const StatsCard = ({ cols }) => {
  const {t} = useTranslation()
  const [popoverOpen, setPopoverOpen] = useState(false)
  const test_page_data = useSelector((store) => store.test_page.charts)
  const chart_length = Object.keys(test_page_data).length
  return (
    <Card className='card-statistics'>
      <CardBody>
        <StatsVertical icon={<AlertOctagon size={21} />} color='info' stats={(chart_length > 0) ? test_page_data.CriticalThreats : ""} statTitle= {t('Possible Zeroday Attacks')} />
      </CardBody>
    </Card>
  )
}

export default StatsCard
