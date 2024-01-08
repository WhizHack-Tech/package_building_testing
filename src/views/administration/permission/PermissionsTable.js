// ** Reactstrap
import Select from 'react-select'
import { Component, Fragment, useState } from 'react'
import { selectThemeColors } from '@utils'
import axios from '@axios'
import { Card, CardHeader, CardTitle, CardSubtitle, Table, CustomInput, Col, Button, DropdownMenu, DropdownItem, DropdownToggle, UncontrolledButtonDropdown, Row, Label, Form } from 'reactstrap'
const colourOptions = [
  { value: 'Admin', label: 'Admin' },
  { value: 'Management', label: 'Management' },
  { value: 'Secuirity', label: 'Security' },
  { value: 'Network', label: 'Network' }
]
const PermissionsTable = () => {

  const url = "/users"
const [data, setData] = useState({
   dash_view: '',
   dash_add: '',
   dash_edit: '',
   dash_delete: '',
   attack_view: '',
   attack_add: '',
   attack_edit: '',
   attack_delete: '',
   asset_view: '',
   asset_add: '',
   asset_edit: '',
   asste_delete: '',
   org_view: '',
   org_add: '',
   org_edit: '',
   org_delete: '',
   config_view: '',
   config_add: '',
   config_edit: '',
   config_delete: '',
   email_view: '',
   eamil_add: '',
   email_edit: '',
   email_delete: '',
   role_view: '',
   role_add: '',
   role_edit: '',
   role_delete: '',
   log_view: '',
   log_add: '',
   log_edit: '',
   log_delete: '',
   third_view: '',
   third_add: '',
   third_edit: '',
   third_delete: '',
   faq_view: '',
   faq_add: '',
   faq_edit: '',
   faq_delete: '',
   base_view: '',
   base_add: '',
   base_edit: '',
   base_delete: '',
   account_view: '',
   account_add: '',
   account_edit: '',
   account_delete: '',
   billing_view: '',
   billing_add: '',
   billing_edit: '',
   billing_delete: ''

})

function submit(e) {
  e.preventDefault()
  axios.post(url, {
   dash_view: data.dash_view,
   dash_add: data.dash_add,
   dash_edit: data.dash_edit,
   dash_delete: data.dash_delete,
   attack_view: data.attack_view,
   attack_add: data.attack_add,
   attack_edit: data.account_edit,
   attack_delete: data.account_delete,
   asset_view: data.asset_view,
   asset_add: data.asset_add,
   asset_edit: data.asset_edit,
   asste_delete: data.asste_delete,
   org_view: data.org_view,
   org_add: data.org_add,
   org_edit: data.org_edit,
   org_delete: data.org_delete,
   config_view: data.config_view,
   config_add: data.config_add,
   config_edit: data.config_edit,
   config_delete: data.config_delete,
   email_view: data.email_view,
   eamil_add: data.email_add,
   email_edit: data.email_edit,
   email_delete: data.email_delete,
   role_view: data.role_view,
   role_add: data.role_add,
   role_edit: data.role_edit,
   role_delete: data.role_delete,
   log_view: data.log_view,
   log_add: data.log_add,
   log_edit: data.log_edit,
   log_delete: data.log_delete,
   third_view: data.third_view,
   third_add: data.third_add,
   third_edit: data.third_edit,
   third_delete: data.third_delete,
   faq_view: data.faq_view,
   faq_add: data.faq_add,
   faq_edit: data.faq_edit,
   faq_delete: data.faq_delete,
   base_view: data.base_view,
   base_add: data.base_add,
   base_edit: data.base_edit,
   base_delete: data.base_delete,
   account_view: data.account_view,
   account_add: data.account_add,
   account_edit: data.account_edit,
   account_delete: data.account_delete,
   billing_view: data.billing_view,
   billing_add: data.billing_add,
   billing_edit: data.billing_edit,
   billing_delete: data.billing_delete
  })
  .then(res => {
    console.log(res.data)
  })
}

function handle(e) {
  const newdata = {...data}
  newdata[e.target.id] = e.target.value
  setData(newdata)
  console.log(newdata)
}
  return (
    <Card>
       <Form onSubmit={(e) => submit(e)}>
         <CardHeader>
        <div>
          <CardTitle className='mb-75' tag='h2'>
          Permissions
          </CardTitle>
          <CardSubtitle className='text-muted'>Permission according to roles</CardSubtitle>
          </div>

            <Col className='mb-0 mt-0' md='2' sm='2'>
            <Label>Roles</Label>
            <Select
              theme={selectThemeColors}
              className='react-select'
              classNamePrefix='select'
              defaultValue={colourOptions[0]}
              options={colourOptions}
              isClearable={false}
            />
          </Col>
        
        
      </CardHeader>
      <Table striped borderless responsive>
        <thead className='thead-light'>
          <tr>
            <th>Module</th>
            <th>View</th>
            <th>Add</th>
            <th>Edit</th>
            <th>Delete</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Dashboard</td>
            <td>
              <CustomInput type='checkbox' id='dash_view' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='dash_add' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='dash_edit' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='dash_delete' onChange={(e) => handle(e)} />
            </td>
          </tr>
          <tr>
            <td>Attacks</td>
            <td>
              <CustomInput type='checkbox' id='attack_view' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='attack_add' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='attack_edit' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='attack_delete' onChange={(e) => handle(e)} />
            </td>
          </tr>
          <tr>
            <td>Assets</td>
            <td>
              <CustomInput type='checkbox' id='asset_view' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='asset_add' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='asset_edit' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='asset_delete' onChange={(e) => handle(e)} />
            </td>
          </tr>
          <tr>
            <td>Organization Settings</td>
            <td>
              <CustomInput type='checkbox' id='org_view' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='org_add' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='org_edit' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='org_delete' onChange={(e) => handle(e)} />
            </td>
          </tr>
          <tr>
            <td>User Config</td>
            <td>
              <CustomInput type='checkbox' id='config_view' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='config_add' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='config_edit' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='config_delete' onChange={(e) => handle(e)} />
            </td>
          </tr>
         <tr>
            <td>Email Config</td>
            <td>
              <CustomInput type='checkbox' id='email_view' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='email_add' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='email_edit' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='email_delete' onChange={(e) => handle(e)} />
            </td>
         </tr>
          <tr>
            <td>Roles</td>
            <td>
              <CustomInput type='checkbox' id='role_view' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='role_add' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='role_edit' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='role_delete' onChange={(e) => handle(e)} />
            </td>
          </tr>
          <tr>
            <td>User Log</td>
            <td>
              <CustomInput type='checkbox' id='log_view' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='log_add' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='log_edit' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='log_delete' onChange={(e) => handle(e)} />
            </td>
          </tr>
          <tr>
            <td>Third Party Integration</td>
            <td>
              <CustomInput type='checkbox' id='third_view' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='third_add' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='third_edit' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='third_delete' onChange={(e) => handle(e)} />
            </td>
          </tr>
          <tr>
            <td>FAQ</td>
            <td>
              <CustomInput type='checkbox' id='faq_view' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='faq_add' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='faq_edit' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='faq_delete' onChange={(e) => handle(e)} />
            </td>
          </tr>
          <tr>
            <td>Knowledge Base</td>
            <td>
              <CustomInput type='checkbox' id='base_view' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='base_add' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='base_edit' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='base_delete' onChange={(e) => handle(e)} />
            </td>
          </tr>
          <tr>
            <td>Edit Account</td>
            <td>
              <CustomInput type='checkbox' id='account_view' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='account_add' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='account_edit' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='account_delete' onChange={(e) => handle(e)} />
            </td>
          </tr>
          <tr>
            <td>Blling Settings</td>
            <td>
              <CustomInput type='checkbox' id='billing_view' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='billing_add' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='billing_edit' onChange={(e) => handle(e)} />
            </td>
            <td>
              <CustomInput type='checkbox' id='billing_delete' onChange={(e) => handle(e)} />
            </td>
          </tr> 
        </tbody>
      </Table> 
      
      <th>
          <div className='float-right ml-2 mb-2 mt-2'>
          <Button.Ripple color='primary' className='btn-next' type='submit'>
            <span className='align-middle d-sm-inline-block d-none'>Submit</span>
          </Button.Ripple>
        </div>
        </th>
 </Form>        
    </Card>
    
  )
}

export default PermissionsTable
