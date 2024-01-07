import classnames from 'classnames'
import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { TrendingUp, User, Box, Aperture, Codesandbox, Codepen, Info } from 'react-feather'
import { Card, CardHeader, CardTitle, CardBody, CardText, Row, Col, Media, Badge, Popover, PopoverHeader, PopoverBody } from 'reactstrap'
import { useState, useEffect } from 'react'
import { useSelector } from "react-redux"
const StatsCard = ({ cols }) => {
  const { t } = useTranslation()
  const chart_data = useSelector((store) => store.test_page.charts)
  const chart_length = Object.keys(chart_data).length
  const [popoverOpen, setPopoverOpen] = useState(false)
  const serviceName = []

  if (chart_length > 0) {
    if (chart_data.ServiceName.length > 0) {
      chart_data.ServiceName.forEach(element => {
        serviceName.push({
          title: element.name,
          subtitle: element.val,
          color: 'light-danger',
          color2: 'light-info'
        })
      })
    }
  }

  const renderData = () => {
    return serviceName.map((item, index) => {
      const margin = Object.keys(cols)
      return (
        <Col
          key={index}
          {...cols}
          md="6"
          className={classnames({
            [`mb-3 mb-1${margin[0]}-0`]: index !== serviceName.length - 2
          })}
        >
          <Media>
            <h4 className='font-weight-bolder mb-0 mr-2'><Badge color={item.color2}>{item.title}</Badge></h4>
            <Media className='my-auto' body>
              <CardText className='d-inline-block'><Badge color={item.color}>{item.subtitle}</Badge></CardText>
            </Media>
          </Media>
        </Col>
      )
    })
  }

  return (
    <Card className='card-statistics'>
      <CardHeader>
        <CardTitle tag='h4'>{t('Top Attacked Services')}</CardTitle>
        <Badge color='primary'>
          <Link><Info id='Most_Attacked_Services' size={20} /></Link>
        </Badge>
        <Popover
          placement='top'
          target='Most_Attacked_Services'
          isOpen={popoverOpen}
          toggle={() => setPopoverOpen(!popoverOpen)}
        >
          <PopoverHeader>{t('Top Attacked Services')}</PopoverHeader>
          <PopoverBody>
            {t('In this card, you will identify the most attacked services by the attacker')}
          </PopoverBody>
        </Popover>
      </CardHeader>
      <CardBody className='statistics-body'>
        <Row>{renderData()}</Row>
      </CardBody>
    </Card>
  )
}

export default StatsCard
