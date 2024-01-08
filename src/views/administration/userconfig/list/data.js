// ================================================================================================
//  File Name: data.js
//  Description: Details of the Administration ( List User Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** Custom Components
import Avatar from '@components/avatar'
import { Link } from 'react-router-dom'
import { useState } from 'react'
import { getUserData } from "@utils"
import axios from '@axios'

// ** Third Party Components
import { User, Mail, Phone, Trello, Eye, Globe } from 'react-feather'
import { Badge, CustomInput, Modal, ModalHeader, ModalBody, FormGroup, ModalFooter, Button, Spinner } from 'reactstrap'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import InputPasswordToggle from '@components/input-password-toggle'

const MySwal = withReactContent(Swal)

// ** Renders Client Columns
const renderClient = row => {
  const stateNum = Math.floor(Math.random() * 6),
    states = ['light-success', 'light-danger', 'light-warning', 'light-info', 'light-primary', 'light-secondary'],
    color = states[stateNum]

  if (row.avatar) {
    return <Avatar className='mr-1' img={row.avatar} width='32' height='32' />
  } else {
    return <Avatar color={color || 'primary'} className='mr-1' content={row.first_name || 'John Doe'} initials />
  }
}
const first_config = {
  0: { title: 'Unverified', color: 'light-warning' },
  1: { title: 'Verified', color: 'light-success' }
}
const role_id_id = {
  2: { title: 'Network Admin', color: 'light-warning' },
  1: { title: 'Super Admin', color: 'light-success' }
}

const status = {
  1: { title: 'Current', color: 'light-primary' },
  2: { title: 'Professional', color: 'light-success' },
  3: { title: 'Rejected', color: 'light-danger' },
  4: { title: 'Resigned', color: 'light-warning' },
  5: { title: 'Applied', color: 'light-info' }
}

const UserAccountStatusModal = ({ row }) => {
  const [basicModal, setBasicModal] = useState(false)
  const [isActive, setIsActive] = useState(row.is_active)
  const [password, setPassword] = useState("")
  const [checkPass, setCheckPass] = useState("")
  const [loading, setLoading] = useState(true)

  const isActionHandle = (event) => {
    setBasicModal(!basicModal)
    setIsActive(event.target.checked)
  }

  const handleClose = () => {
    setBasicModal(!basicModal)
    setIsActive(!isActive)
  }

  const handleChangeStatus = () => {
    const { email } = getUserData()
    if (password !== "") {
      setLoading(false)
      axios.post("/disable-user", {
        user_id: row.id,
        is_active: isActive,
        email,
        password
      }).then((res) => {
        if (res.data.message_type === "success") {
          setIsActive(res.data.is_status)
          setBasicModal(!basicModal)
          MySwal.fire({
            icon: 'success',
            title: "Sit Back and Relax",
            text: 'Great Success',
            customClass: {
              confirmButton: 'btn btn-primary'
            },
            buttonsStyling: false
          })
        }

        setLoading(true)        
      }).catch((error) => {
        if (error.response) {
          if (error.response.data.message_type === "password_incorrect") {
            setIsActive(row.is_active)
            setCheckPass("Please Enter Password Correctly")
          }          
        }

        setLoading(true)
      })

    } else {
      setCheckPass("Field cannot be blank")
    }   
  }
  
  return (
    <div>
      <CustomInput type='switch' id={`id-${row.id}`} checked={isActive} onChange={isActionHandle} />
      <Modal isOpen={basicModal} toggle={() => setBasicModal(!basicModal)} backdrop="static" keyboard={false}>
        <ModalHeader>Enter Your Login Password</ModalHeader>
        <ModalBody>
        <p><Badge color='warning'>{checkPass}</Badge></p>
        <FormGroup>
          <InputPasswordToggle onChange={(e) => { setPassword(e.target.value) }} htmlFor='basic-default-password' />
        </FormGroup>
        </ModalBody>
        <ModalFooter>
          <div>
          <Button.Ripple color='danger' onClick={handleClose} className='btn-submit mr-1'>Close</Button.Ripple>
            {loading ? <Button.Ripple color='primary' onClick={handleChangeStatus}>Save</Button.Ripple> : <Button.Ripple type="button" color='primary' disabled> <Spinner size="sm" />&nbsp;Save...</Button.Ripple>}
          </div>
        </ModalFooter>
      </Modal>
    </div>
  )
}

// ** Table Common Column
export const columns = [
  {
    name: 'Full Name',
    minWidth: '350px',
    selector: 'first_name',
    sortable: true,
    cell: row => (
      <div className='d-flex justify-content-left align-items-center'>
        {renderClient(row)}
        <div className='d-flex flex-column'>
            <span className='font-weight-bold'>{row.first_name} {row.last_name}</span>
          <small className='text-truncate text-muted mb-0'>@ {row.email}</small>
        </div>
      </div>
    )
  },
  // {
  //   name: 'Last Name',
  //   minWidth: '150px',
  //   selector: 'last_name',
  //   sortable: true,
  //   cell: row => {
  //     return (
  //       <div className='d-flex justify-content-left align-items-center'>
  //         <User size={15} className='mb-0' />
  //         <span className='font-weight-bold ml-1'>{row.last_name}</span>
  //       </div>
  //     )
  //   }
  // },
  {
    name: 'Email',
    minWidth: '350px',
    selector: 'email',
    sortable: true,
    cell: row => {
      return (
        <div className='d-flex justify-content-left align-items-center'>
          <Mail size={15} className='mb-0' />
          <span className='font-weight-bold ml-1'>{row.email}</span>
        </div>
      )
    }
  },
  {
    name: 'Branch Code',
    minWidth: '200px',
    selector: 'location_branchcode',
    sortable: true,
    cell: row => {
      return (
        <div className='d-flex justify-content-left align-items-center'>
          <Globe size={15} className='mb-0' />
          <span className='font-weight-bold ml-1'>{row.location_branchcode}</span>
        </div>
      )
    }
  },
  {
    name: 'Status',
    minWidth: '50px',
    selector: 'first_config',
    sortable: true,
    cell: row => {
      return (
        <Badge color={first_config[row.first_config].color} pill>
          {first_config[row.first_config].title}
        </Badge>
      )
    }
  },
  {
    name: 'Role',
    minWidth: '50px',
    selector: 'role_id_id',
    sortable: true,
    cell: row => {
      return (
        <Badge color={role_id_id[row.role_id_id || 2].color} pill>
          {row.role_id_id ? role_id_id[row.role_id_id].title : null}
        </Badge>
      )
    }
  },
  {
    name: 'Phone',
    minWidth:"200px",
    selector: 'contact_number',
    sortable: true,
    cell: row => {
      return (
        <div className='d-flex justify-content-left align-items-center'>
          <Phone size={15} className='mb-0' />
          <span className='font-weight-bold ml-1'>{row.contact_number}</span>
        </div>
      )
    }
  },
  {
    name: 'Company Name',
    minWidth: '300px',
    selector: 'organization_name',
    sortable: true,
    cell: row => {
      return (
        <div className='d-flex justify-content-left align-items-center'>
          <Trello size={15} className='mb-0' />
          <span className='font-weight-bold ml-1'>{row.organization_name}</span>
        </div>
      )
    }
  },
  {
    name: 'Account Active Status',
    minWidth: '100px',
    selector: '',
    sortable: true,
    cell: row => <UserAccountStatusModal row={row} />
  },
  {
    name: 'Actions',
    minWidth: '100px',
    sortable: true,
    cell: row => (
      <div className='column-action d-flex align-items-center'>
        <Link to={`/administration/userconfig/view/${row.id}`} id={`pw-tooltip-${row.id}`}>
          <Eye size={17} className='mx-1' />
        </Link>
      </div>
    )
  }
]
export default columns
