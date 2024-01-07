// =============================================================================================
//  File Name: widgets\stats\Botnet.js
//  Description: Details of the botnet component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** Third Party Components
import { Badge, Card, CardBody } from 'reactstrap'
import Critical from "../../../../assets/images/svg/Critical.svg"
import Avatar from '@components/avatar'

const Botnet = ({ stats, statTitle, className, ...rest }) => {
  return (
    <Card className='text-center'>
      <CardBody className={className}>
      <Avatar color='light-primary' icon={<img width={40} src={Critical} />} size='lg'/>
        <h2 className='font-weight-bolder'>{stats}</h2>
        <p className='card-text line-ellipsis'>{statTitle}</p>
      </CardBody>
    </Card>
  )
}

export default Botnet
