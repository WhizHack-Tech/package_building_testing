// =============================================================================================
//  File Name: widgets\stats\StatsVertical.js
//  Description: Details of the stats Vertical component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** Third Party Components
import PropTypes from 'prop-types'
import { Badge, Card, CardBody } from 'reactstrap'
import Critical from "../../../../assets/images/svg/Botnet.svg"
import Avatar from '@components/avatar'

const StatsVertical = ({ stats, statTitle, className}) => {
  return (
    <Card className='text-center'>
      <CardBody className={className}>
      <Avatar color='light-info' icon={<img width={40} src={Critical} />} size='lg'/>
        <h2 className='font-weight-bolder'>{stats}</h2>
        <p className='card-text line-ellipsis'>{statTitle}</p>
      </CardBody>
    </Card>
  )
}

export default StatsVertical

