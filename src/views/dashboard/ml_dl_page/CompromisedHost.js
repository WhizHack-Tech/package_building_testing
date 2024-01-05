import { Link } from 'react-router-dom'
import { TrendingUp, User, Box, Info, Sunset, MessageSquare } from 'react-feather'
import { Card, CardHeader, CardTitle, CardBody, CardText, Row, Col, Media, Button, Popover, PopoverHeader, PopoverBody, Badge } from 'reactstrap'
import { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useTranslation } from 'react-i18next'
import StatsVertical from '@components/widgets/stats/Botnet'
const StatsCard = ({ cols }) => {
  const {t} = useTranslation()
  const [popoverOpen, setPopoverOpen] = useState(false)
  const test_page_data = useSelector((store) => store.test_page.charts)
  const chart_length = Object.keys(test_page_data).length
  return (
    <Card className='card-statistics'>
      <CardBody>
        <StatsVertical icon={<Sunset size={21} />} color='primary' stats={(chart_length > 0) ? test_page_data.InternalCompromisedAttackCount : ""} statTitle={t('Internal Attack Count')} />
      </CardBody>
    </Card>
  )
}

export default StatsCard
