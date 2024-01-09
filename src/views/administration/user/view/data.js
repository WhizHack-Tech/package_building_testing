// ================================================================================================
//  File Name: data.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
// ** Custom Components
import Avatar from '@components/avatar'
import { useState, useEffect, Fragment } from 'react'
import { ChevronDown, ChevronRight, EyeOff, Eye } from 'react-feather'
import { Badge, Row, TabContent, TabPane, Nav, NavItem, NavLink, Collapse, CardHeader, CardTitle, CardBody, Col } from 'reactstrap'


// ** Vars
const states = ['success', 'danger', 'warning', 'info', 'dark', 'primary', 'secondary']

const role_id = {
  2: { title: 'Network Admin', color: 'light-warning' },
  1: { title: 'Super Admin', color: 'light-success' }
}

const first_config = {
  0: { title: 'Unverified', color: 'light-warning' },
  1: { title: 'Verified', color: 'light-success' }
}

// ** Renders Client Columns
const renderClient = row => {
  const stateNum = Math.floor(Math.random() * 6),
    states = ['light-success', 'light-danger', 'light-warning', 'light-info', 'light-primary', 'light-secondary'],
    color = states[stateNum]

  if (row.avatar) {
    return <Avatar className='mr-1' img={row.avatar} width='20' height='20' />
  } else {
    return <Avatar color={color || 'primary'} className='mr-1' content={row.username || 'John Doe'} initials />
  }
}
// ** Table Zero Config Column
export const basicColumns = [
  {
    name: 'FullName',
    selector: 'username',
    sortable: true,
    maxWidth: '500px',
    cell: row => (
      <div className='d-flex justify-content-left align-items-center'>
        {renderClient(row)}
        <div className='d-flex flex-column'>
          <span className='font-weight-bold'>{row.username}</span>
        </div>
      </div>
    )
  },
  {
    name: 'Email',
    selector: 'email',
    sortable: true,
    minWidth: '150px'
  },
  {
    name: 'Role',
    selector: 'role_id',
    sortable: true,
    minWidth: '70px',
    cell: row => {
      return (
        <Badge color={role_id[row.role_id].color} pill>
          {role_id[row.role_id].title}
        </Badge>
      )
    }
  },
  {
    name: 'Status',
    selector: 'first_config',
    sortable: true,
    minWidth: '50px',
    cell: row => {
      return (
        <Badge color={first_config[row.first_config].color} pill>
          {first_config[row.first_config].title}
        </Badge>
      )
    }
  },
  {
    name: 'Phone',
    selector: 'contact_number',
    sortable: true,
    minWidth: '100px'
  },
  {
    name: 'Join Date',
    selector: 'created_at',
    sortable: true,
    minWidth: '100px',
    cell: row => {
      return (
        <div className='d-flex justify-content-left align-items-center'>
          <Badge color='light-primary'>
            <span className='font-weight-bold'>{new Date(row.created_at).toDateString()}</span>
          </Badge>
        </div>
      )
    }
  }
]

export const columns = [
  {
    name: 'FullName',
    selector: 'username',
    sortable: true,
    maxWidth: '500px'
  },
  {
    name: 'Email',
    selector: 'email',
    sortable: true,
    minWidth: '150px'
  },
  {
    name: 'Role',
    selector: 'role_id',
    sortable: true,
    minWidth: '70px'
  },
  {
    name: 'Status',
    selector: 'first_config',
    sortable: true,
    minWidth: '50px'
  },
  {
    name: 'Phone',
    selector: 'contact_number',
    sortable: true,
    minWidth: '100px'
  },
  {
    name: 'Join Date',
    selector: 'created_at',
    sortable: true,
    minWidth: '100px',
    cell: row => {
      return (
        <div className='d-flex justify-content-left align-items-center'>
          <Badge color='light-primary'>
            <span className='font-weight-bold'>{new Date(row.created_at).toDateString()}</span>
          </Badge>
        </div>
      )
    }
  }
]

const ExpandableTable = ({ data }) => {
  const [active, setActive] = useState('1')
  const [isOpen, setIsOpen] = useState(true)
  const [Isopen, setIsopen] = useState(true)
  const [isOpen1, setIsOpen1] = useState(true)
  const [pass, setPass] = useState(false)

  const toggle = tab => {
    if (active !== tab) {
      setActive(tab)
    }
  }
  return (

    <Fragment>
      <div className='expandable-content'>
        <Nav tabs>
          <NavItem>
            <NavLink
              active={active === '1'}
              onClick={() => {
                toggle('1')
              }}
            >
              Config Details
            </NavLink>
          </NavItem>
          <NavItem>
            <NavLink
              active={active === '2'}
              onClick={() => {
                toggle('2')
              }}
            >
              Product Pages
            </NavLink>
          </NavItem>
        </Nav>
        <TabContent className='py-50 ml-1' activeTab={active}>
          <TabPane tabId='1'>
            <div>
              <CardHeader>
                <CardTitle tag='h4' onClick={() => { setIsOpen(!isOpen) }}> <div className='views cursor-pointer d-inline-block pr-1'>
                  {isOpen ? <ChevronDown size='18' /> : <ChevronRight size='18' />}
                </div>
                  Dashboard Config</CardTitle>

              </CardHeader>
              <Collapse isOpen={isOpen}>
                <hr />
                <CardBody>
                  <Row>
                    <Col xs={1} md={3}> Platform : <Badge color='primary'>data</Badge></Col>
                    <Col xs={1} md={3}> Threat Severity : <Badge color='secondary'>data</Badge></Col>
                    <Col xs={1} md={3}> Accuracy : <Badge color='warning'>data</Badge></Col>
                    <Col xs={1} md={3}> Trace : <Badge color='warning'>data</Badge></Col>
                  </Row>
                </CardBody>
              </Collapse>
              <hr />
            </div>
            <div>
              <CardHeader>
                <CardTitle tag='h4' onClick={() => { setIsopen(!Isopen) }}> <div className='views cursor-pointer d-inline-block pr-1'>
                  {Isopen ? <ChevronDown size='18' /> : <ChevronRight size='18' />}
                </div>
                  Email Config</CardTitle>

              </CardHeader>
              <Collapse isOpen={Isopen}>
                <hr />
                <CardBody mt='1'>
                  <Row >
                    <Col xs={1} md={3}> Select Email : <Badge color='light-primary'>{data.contact}</Badge></Col>
                    <Col xs={1} md={3}> Platform : <Badge color='light-warning'>data</Badge></Col>
                    <Col xs={1} md={3}> Threat Severity : <Badge color='light-warning'>data</Badge></Col>
                    <Col xs={1} md={3}> Accuracy : <Badge color='light-warning'>data</Badge></Col>
                    <Col xs={1} md={3} style={{ marginTop: '15px' }}> Trace : <Badge color='light-warning'>data</Badge></Col>
                  </Row>
                </CardBody>
              </Collapse>
              <hr />
            </div>
            <div>
              <CardHeader>
                <CardTitle tag='h4' onClick={() => { setIsOpen1(!isOpen1) }}> <div className='views cursor-pointer d-inline-block pr-1'>
                  {isOpen1 ? <ChevronDown size='18' /> : <ChevronRight size='18' />}
                </div>
                  Notification Config</CardTitle>

              </CardHeader>
              <Collapse isOpen={isOpen1}>
                <hr />
                <CardBody>
                  <Row>
                    <Col xs={1} md={3}> Platform : <Badge color='light-warning'>data</Badge></Col>
                    <Col xs={1} md={3}> Threat Severity : <Badge color='light-warning'>data</Badge></Col>
                    <Col xs={1} md={3}> Accuracy : <Badge color='light-warning'>data</Badge></Col>
                    <Col xs={1} md={3}> Time Interval : <Badge color='light-warning'>data</Badge></Col>
                    <Col xs={1} md={3} style={{ marginTop: '15px' }}> Trace : <Badge color='light-warning'>data</Badge></Col>
                  </Row>
                </CardBody>
              </Collapse>
              <hr />
            </div>
            <div>
              <CardHeader>
                <CardTitle tag='h4' onClick={() => { setIsOpen1(!isOpen1) }}> <div className='views cursor-pointer d-inline-block pr-1'>
                  {isOpen1 ? <ChevronDown size='18' /> : <ChevronRight size='18' />}
                </div>
                  Attach Agent</CardTitle>

              </CardHeader>
              <Collapse isOpen={isOpen1}>
                <hr />
                <CardBody>
                  <Row>
                    <Col xs={1} md={5}> Database username : <Badge color='light-warning'>data</Badge></Col>
                    <Col xs={1} md={5}> Database Port : <Badge color='light-warning'>data</Badge></Col>
                    <Col xs={1} md={5} style={{ marginTop: '15px' }}> Database Host : <Badge color='light-warning'>data</Badge></Col>
                    <Col xs={1} md={5} style={{ marginTop: '15px' }}> Database Password :
                      <span className='font-weight-bold ml-1'>{pass ? data.db_password : "*******"}</span>&nbsp;&nbsp;
                      <span onClick={() => { setPass(!pass) }} className='ml-1'><Badge color='light-primary'>{pass ? <Eye size={15} /> : <EyeOff size={15} />}</Badge></span>
                    </Col>
                  </Row>
                </CardBody>
              </Collapse>
              <hr />
            </div>
          </TabPane>
          <TabPane tabId='2'>
          <CardBody>
                  <Row>
                    <Col xs={1} md={3}> Default Page : <Badge color='primary'>data</Badge></Col>
                    <Col xs={1} md={3}> Trace : <Badge color='secondary'>data</Badge></Col>
                    <Col xs={1} md={3}> Wazuh : <Badge color='warning'>data</Badge></Col>
                    <Col xs={1} md={3} style={{ marginTop: '15px' }}> HIDS : <Badge color='warning'>data</Badge></Col>
                    <Col xs={1} md={3} style={{ marginTop: '15px' }}> NIDS : <Badge color='warning'>data</Badge></Col>
                  </Row>
                </CardBody>
          </TabPane>
        </TabContent>
      </div>
    </Fragment>
  )
}

export default ExpandableTable
