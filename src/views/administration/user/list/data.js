// ================================================================================================
//  File Name: data.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** Custom Components
import Avatar from '@components/avatar'
import { Link } from 'react-router-dom'
import { Mail, Phone, Trello, Eye, Calendar, MapPin, Zap } from 'react-feather'
import { Badge, CustomInput, Modal, ModalHeader, ModalBody, FormGroup, ModalFooter, Button, Spinner } from 'reactstrap'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import { useState } from 'react'
import { getUserData } from "@utils"
import axios from '@axios'
import InputPasswordToggle from '@components/input-password-toggle'

const MySwal = withReactContent(Swal)

// ** Renders Client Columns
const renderClient = row => {
  const stateNum = Math.floor(Math.random() * 6),
    states = ['light-success', 'light-danger', 'light-warning', 'light-info', 'light-primary', 'light-secondary'],
    color = states[stateNum]

  if (row.avatar) {
    return <Avatar className='mr-1' img={row.avatar} width='40' height='32' />
  } else {
    return <Avatar color={color || 'primary'} className='mr-1' content={row.organization_name || 'John Doe'} initials />
  }
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
      axios.post("/disable-org", {
        org_id: row.organization_id,
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
          console.log(error.response.data.message)
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
    name: 'Actions',
    minWidth: '100px',
    sortable: true,
    cell: row => (
      <div className='column-action d-flex align-items-center'>
        <Link to={`/administration/user/view/${row.id}/${row.activated_plan_id}`} id={`pw-tooltip-${row.id}`}>
          <Eye size={17} className='mx-1' />
        </Link>
      </div>
    )
  },
  {
    name: 'Organization Name',
    minWidth: '300px',
    selector: 'organization_name',
    sortable: true,
    cell: row => (
      <div className='d-flex justify-content-left align-items-center'>
        {renderClient(row)}
        <div className='d-flex flex-column'>
            <span className='font-weight-bold'>{row.organization_name}</span>
        </div>
      </div>
    )
  },
  {
    name: 'Location Name',
    minWidth: '250px',
    selector: '',
    sortable: true,
    cell: row => {
      return (
        <div className='d-flex justify-content-left align-items-center'>
          <Trello size={15} className='mb-0' />
          <span className='font-weight-bold ml-1'>{row.city}-{row.branchcode}</span>
        </div>
      )
    }
  },
  {
    name: 'Email',
    minWidth: '250px',
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
    name: 'Phone',
    minWidth: '200px',
    selector: 'phone_number',
    sortable: true,
    cell: row => {
      return (
        <div className='d-flex justify-content-left align-items-center'>
          <Phone size={15} className='mb-0' />
          <span className='font-weight-bold ml-1'>{row.phone_number}</span>
        </div>
      )
    }
  },
  {
    name: 'City',
    minWidth: '150px',
    selector: 'city',
    sortable: true,
    cell: row => {
      return (
        <div className='d-flex justify-content-left align-items-center'>
          <MapPin size={15} className='mb-0' />
          <span className='font-weight-bold ml-1'>{row.city}</span>
        </div>
      )
    }
  },
  {
    name: 'BranchCode',
    minWidth: '200px',
    selector: 'branchcode',
    sortable: true,
    cell: row => {
      return (
        <div className='d-flex justify-content-left align-items-center'>
          <Zap size={15} className='mb-0' />
          <span className='font-weight-bold ml-1'>{row.branchcode}</span>
        </div>
      )
    }
  },
  {
    name: 'Activation Date',
    minWidth: '250px',
    selector: 'created_at',
    sortable: true,
    cell: row => {
      return (
        <div className='d-flex justify-content-left align-items-center'>
          <Calendar size={15} className='mb-0' />
          <span className='font-weight-bold ml-1'>{new Date(row.created_at).toDateString()}</span>
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
  }
]
export default columns
