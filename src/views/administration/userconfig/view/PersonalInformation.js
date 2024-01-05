// ================================================================================================
//  File Name:  Personalinformation.js
//  Description: User Config Details.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================

import {  Row, Col, Button, Form, Input, Label, FormGroup, Table, CustomInput, Spinner, CardBody, CardHeader, CardTitle } from 'reactstrap'
import { useTranslation } from 'react-i18next'
const UserAccountTab = ({selectedUser}) => {
  const {t} = useTranslation()
    return (
       (selectedUser === null) ? `Logining..` :  <Row>
         <CardHeader>
          <CardTitle tag='h2'>{t('Address Details')}</CardTitle>
        </CardHeader>
        <CardBody>
    <Col sm='12'>
        <Form>
            <Row>
              <Col sm='6'>
                <FormGroup>
                  <Label>{t('Address-1')}</Label>
                  <Input type='text' disabled value={selectedUser.address_1} />
                </FormGroup>
              </Col>  
              <Col sm='6'>
                <FormGroup>
                  <Label>{t('Address-2')}</Label>
                  <Input type='text' disabled value={selectedUser.address_2} />
                </FormGroup>
              </Col>  
              <Col sm='6'>
                <FormGroup>
                  <Label>{t('State')}</Label>
                  <Input type='text' disabled value={selectedUser.state} />
                </FormGroup>
              </Col>
              <Col sm='6'>
                <FormGroup>
                  <Label>{t('City')}</Label>
                  <Input type='text' disabled value={selectedUser.city} />
                </FormGroup>
              </Col>  
              <Col sm='6'>
                <FormGroup>
                  <Label>{t('Zipcode')}</Label>
                  <Input type='text' disabled value={selectedUser.zipcode} />
                </FormGroup>
              </Col>           
            </Row>
          </Form>
        </Col>
        </CardBody>
      </Row>
     
    )
  }

export default UserAccountTab
