import classnames from 'classnames'
import { Link } from 'react-router-dom'
import Avatar from '@components/avatar'
import { TrendingUp, User, Box, DollarSign, Info, Eye, Cpu, AlertOctagon } from 'react-feather'
import { Card, CardHeader, CardTitle, CardBody, CardText, Row, Col, Media, Button, Popover, PopoverHeader, PopoverBody, Badge } from 'reactstrap'
import { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import CuIcon from "../../../assets/images/svg/ids.svg"
import CIcon from "../../../assets/images/svg/ml.svg"
import Dl from "../../../assets/images/svg/dl.svg"
import { FormattedMessage } from 'react-intl'
const StatsCard = ({ cols }) => {
  const dashboard_charts_data = useSelector((store) => store.dashboard_charts.charts)
  const [popoverOpen, setPopoverOpen] = useState(false)

  const chart_length = Object.keys(dashboard_charts_data).length
  let data = []
  if (chart_length > 0) {
    data = [
      {
        title: dashboard_charts_data.SeverityCount.severity_1_count,
        subtitle: <FormattedMessage id='Severity 1' />,
        color: 'primary',
        color: 'danger',
        icon: <AlertOctagon size={30} />
      },
      {
        title: dashboard_charts_data.SeverityCount.severity_2_count,
        subtitle: <FormattedMessage id='Severity 2' />,
        color: 'primary',
        icon: <AlertOctagon size={30} />
      },
      {
        title: dashboard_charts_data.SeverityCount.severity_3_count,
        subtitle: <FormattedMessage id='Severity 3' />,
        color: 'info',
        icon: <AlertOctagon size={30} />
      }
    ]
  } else {
    data = [
      {
        title: 0,
        subtitle: <FormattedMessage id='Ml Detection' />,
        color: 'primary',
        icon: <img width={30} src={CIcon} />
      },
      {
        title: 0,
        subtitle: <FormattedMessage id='DL Detection' />,
        color: 'info',
        icon: <img width={30} src={Dl} />
      },
      {
        title: 0,
        subtitle: <FormattedMessage id='IDS Detection' />,
        color: 'danger',
        icon: <img width={30} src={CuIcon} />
      }
    ]
  }

  const renderData = () => {
    return data.map((item, index) => {
      const margin = Object.keys(cols)
      return (
        <Col
          key={index}
          {...cols}
          className={classnames({
            [`mb-2 mb-${margin[0]}-0`]: index !== data.length - 1
          })}
        >
          <Media>
            <Avatar color={item.color} icon={item.icon} className='mr-2' />
            <Media className='my-auto mb-4' body>
              <h4 className='font-weight-bolder mb-0'>{item.title}</h4>
              <CardText className='font mb-0'>{item.subtitle}</CardText>
            </Media>
          </Media>
        </Col>

      )
    })
  }

  return (
    <Card className='card-statistics'>
      <CardHeader>
        <CardTitle tag='h4'><FormattedMessage id='Threat Detection Type' /></CardTitle>
        <Badge color='primary'>
          <Link><Info id='Threat_Detection_Type' size={20} /></Link>
        </Badge>
        <Popover
          placement='top'
          target='Threat_Detection_Type' s
          isOpen={popoverOpen}
          toggle={() => setPopoverOpen(!popoverOpen)}
        >
          <PopoverHeader><FormattedMessage id='Threat Detection Type' /></PopoverHeader>
          <PopoverBody>
          <FormattedMessage id='This card represents the count of the different detection mechanisms.' />
          </PopoverBody>
        </Popover>
      </CardHeader>
      <CardBody className='statistics-body'>
        <Row className='mt-2'>{renderData()}</Row>
      </CardBody>
    </Card>
  )
}

export default StatsCard