// =============================================================================================
//  File Name: widgets\stats\internal.js
//  Description: Details of the internal component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** Third Party Components
import { Badge, Card, CardBody } from 'reactstrap'
import internal from "../../../../assets/images/svg/internal.svg"
import Avatar from '@components/avatar'

const Internal = ({ stats, statTitle, className, ...rest }) => {
  return (
    <Card className='text-center'>
      <CardBody className={className}>
      <Avatar color='light-danger' icon={<img width={40} src={internal} />} size='lg'/>
        <h2 className='font-weight-bolder'>{stats}</h2>
        <p className='card-text line-ellipsis'>{statTitle}</p>
      </CardBody>
    </Card>
  )
}

export default Internal
