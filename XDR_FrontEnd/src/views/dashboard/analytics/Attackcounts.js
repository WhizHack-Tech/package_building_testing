import classnames from 'classnames'
import Avatar from '@components/avatar'
import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { TrendingUp, User, Box, Aperture, Codesandbox, Codepen, Info } from 'react-feather'
import { Card, CardHeader, CardTitle, CardBody, CardText, Row, Col, Media, Badge, Popover, PopoverHeader, PopoverBody } from 'reactstrap'
import { useState, useEffect } from 'react'
import attacks from "../../../assets/images/svg/attacks.svg"
import { useSelector } from "react-redux"
const StatsCard = ({ cols }) => {
  const {t} = useTranslation()
  const chart_data = useSelector((store) => store.attack_evnets_charts.charts)
  const chart_length = Object.keys(chart_data).length
  const [popoverOpen, setPopoverOpen] = useState(false)
  const serviceName = []

  if (chart_length > 0) {
    if (chart_data.ServiceName.length > 0) {    
      chart_data.ServiceName.forEach(element => {
        serviceName.push({
          title: element.name,
          subtitle:element.val,
          color: 'light-danger',
          icon: <img width={50} src={attacks} />
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
          className={classnames({
            [`mb-2 mb-${margin[0]}-0`]: index !== serviceName.length - 1
          })}
        >
            <Media>
              <Avatar color={item.color} icon={item.icon} className='mr-1' />
              <Media className='my-auto' body>
                <h4 className='font-weight-bolder mb-0'><Badge color={item.color}>{item.title}</Badge></h4>
                <CardText className='font-small-8 mb-0'><Badge color={item.color}>{item.subtitle}</Badge></CardText>
              </Media>
            </Media>
        </Col>
      )
    })
  }

  return (
    <Card className='card-statistics'>
      <CardHeader>
        <CardTitle>
          {t('Top Attacked Services')}
          </CardTitle>
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
