// ================================================================================================
//  File Name: PasswordtabContent.js
//  Description: Details of the Edit Account Pages.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { FormGroup, Row, Col, Button } from 'reactstrap'
import InputPasswordToggle from '@components/input-password-toggle'
import { AvForm, AvInput } from 'availity-reactstrap-validation-safe'

const PasswordTabContent = () => {
  return (
    <AvForm onSubmit={e => e.preventDefault()}>
      <h6 className='section-label mx-0 mb-1'>Password</h6>
      <Row>
        <Col sm='6'>
          <FormGroup>
            <InputPasswordToggle
              tag={AvInput}
              className='input-group-merge'
              label='Old Password'
              htmlFor='old-password'
              name='old-password'
              required
            />
          </FormGroup>
        </Col>
        <Col sm='6'>
          <FormGroup>
            <InputPasswordToggle
              tag={AvInput}
              className='input-group-merge'
              label='New Password'
              htmlFor='new-password'
              name='new-password'
              required
            />
          </FormGroup>
        </Col>
        <Col sm='6'>
          <FormGroup>
            <InputPasswordToggle
              tag={AvInput}
              className='input-group-merge'
              label='Retype New Password'
              htmlFor='retype-new-password'
              name='retype-new-password'
              required
            />
          </FormGroup>
        </Col>
        <Col className='mt-1' sm='12'>
          <Button.Ripple className='mr-1' color='primary'>
            Save changes
          </Button.Ripple>
        </Col>
      </Row>
    </AvForm>
  )
}

export default PasswordTabContent
