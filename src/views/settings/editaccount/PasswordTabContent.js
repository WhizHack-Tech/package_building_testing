import { FormGroup, Row, Col, Button, CustomInput } from 'reactstrap'
import InputPasswordToggle from '@components/input-password-toggle'
import { AvForm, AvInput } from 'availity-reactstrap-validation-safe'
import { useState } from 'react'
const PasswordTabContent = () => {
  // const [commentOnArticle, setCommentOnArticle] = useState(data.commentOnArticle)
  
  return (
    <AvForm >
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
      </Row>
      <Row>
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
        </Row>
        <Row>
        <Col sm='12' className='mb-2'>
          <CustomInput
            type='switch'
            id='commentOnArticle'
            // checked={commentOnArticle}
            // onChange={e => setCommentOnArticle(e.target.checked)}
            name='customSwitch'
            label='Want to Enable Two Factor Authentication '
          />
        </Col>
      </Row>
      <Row>
        <Col className='mt-1' sm='12'>
          <Button.Ripple className='mr-1' color='primary'>
            Save changes
          </Button.Ripple>
          <Button.Ripple color='secondary' outline>
            Cancel
          </Button.Ripple>
        </Col>
      </Row>
    </AvForm>
  )
}

export default PasswordTabContent
