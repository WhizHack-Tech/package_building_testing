// ================================================================================================
//  File Name: InfoTabContent.js
//  Description: Details of the Discover Data.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ============================================================================================== 
import { Row, Spinner, Col, Button, Form, Input, Label, FormGroup, CardBody, CardHeader, CardTitle, Card } from 'reactstrap'
import { useState, useEffect } from 'react'
import axios from '@axios'
import { token } from '@utils'
import { toast } from 'react-toastify'
import { useTranslation } from 'react-i18next'
const UserAccountTab = ({ data }) => {
  const {t} = useTranslation()
  const [loading, setLoading] = useState(false)

  const formSubmit = (event) => {
    event.preventDefault()
    setLoading(true)
    const formData = new FormData(event.target)
    axios("/account-information-update", {
      method: "post",
      data: formData,
      headers: { Authorization: token() }
    })
      .then(res => {
        setLoading(false)
        if (res.data.message_type === "updated") {
          toast.success(`Information Updated`, {
            position: "top-right",
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined
          })
        }
      }).catch(err => {
        setLoading(false)
      })
  }

  return (
    <Card>
      <h6 className='section-label mx-0 mb-1'>{t('Information')}</h6>
      <Form onSubmit={formSubmit}>
        <div style={{ height: '255px' }}>
          <Row>
            <Col sm='6'>
              <FormGroup>
                <Label>{t('Address-1')}</Label>
                <Input type='text' name="address_1" defaultValue={data.address_1} />
              </FormGroup>
            </Col>
            <Col sm='6'>
              <FormGroup>
                <Label>{t('Address-2')}</Label>
                <Input type='text' name="address_2" defaultValue={data.address_2} />
              </FormGroup>
            </Col>
            <Col sm='6'>
              <FormGroup>
                <Label>{t('State')}</Label>
                <Input type='text' name="state" defaultValue={data.state} />
              </FormGroup>
            </Col>
            <Col sm='6'>
              <FormGroup>
                <Label>{t('City')}</Label>
                <Input type='text' name="city" defaultValue={data.city} />
              </FormGroup>
            </Col>
            <Col sm='6'>
              <FormGroup>
                <Label>{t('Zipcode')}</Label>
                <Input type='text' name="zipcode" defaultValue={data.zipcode} />
              </FormGroup>
            </Col>
            <Col className='mt-1' sm='12'>
              {(loading === false) ? <Button.Ripple color='primary' type="submit">{t('Save Changes')}</Button.Ripple> : <Button.Ripple type="button" color='primary' disabled> <Spinner size="sm" />&nbsp;{t('Saving')}...</Button.Ripple>}
            </Col>
          </Row>
        </div>
      </Form>
    </Card>
  )
}

export default UserAccountTab
