// ================================================================================================
//  File Name: indPlanCardex.js
//  Description: Details of the Administration ( View User Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** Reactstrap
import { Card, CardHeader, CardBody, Badge, UncontrolledTooltip, Button } from 'reactstrap'

const PlanCard = ({ selectedUser }) => {
  return (
    <Card className='plan-card border-primary'>
      <CardHeader className='d-flex justify-content-between align-items-center pt-75 pb-1'>
        <h5 className='mb-0'>Organization Details</h5>
        <Badge id='plan-expiry-date' color='light-secondary'>
          Nov 15, {new Date().getFullYear()}
        </Badge>
      </CardHeader>
      <CardBody>
        <Badge className='text-capitalize' color='light-primary'>
          {selectedUser !== null ? selectedUser.currentPlan : 'Basic'}
        </Badge>
        <ul className='list-unstyled my-1'>
          <li>
            <span className='align-middle'>Whizhack Technology Pvt Ltd</span>
          </li>
          <li className='my-25'>
            <span className='align-middle'>5 Active Sensors</span>
          </li>
          <li>
            <span className='align-middle'>Total 3 Users</span>
          </li>
        </ul>
        {/*<Button.Ripple className='text-center' color='primary' disabled>
          Upgrade Plan
  </Button.Ripple>*/}
      </CardBody>
    </Card>
  )
}

export default PlanCard
