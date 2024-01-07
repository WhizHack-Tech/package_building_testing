// =============================================================================================
//  File Name: widgets\stats\External.js
//  Description: Details of the External component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** Third Party Components
import { Badge, Card, CardBody } from 'reactstrap'
import external from "../../../../assets/images/svg/external.svg"
import Avatar from '@components/avatar'

const External = ({ stats, statTitle, className, ...rest }) => {
  return (
    <Card className='text-center'>
      <CardBody className={className}>
      <Avatar color='light-warning' icon={<img width={40} src={external} />} size='lg'/>
        <h2 className='font-weight-bolder'>{stats}</h2>
        <p className='card-text line-ellipsis'>{statTitle}</p>
      </CardBody>
    </Card>
  )
}

export default External