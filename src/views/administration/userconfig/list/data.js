// ================================================================================================
//  File Name: data.js
//  Description: User Config Details.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================    
import { useState } from 'react'
import Avatar from '@components/avatar'
import { Link } from 'react-router-dom'
import InputPasswordToggle from '@components/input-password-toggle'
import { Mail, Phone, Eye } from 'react-feather'
import { Badge, CustomInput, Modal, ModalHeader, ModalFooter, Button, FormGroup, Spinner, Col, ModalBody } from 'reactstrap'
import axios, { staticPath } from '@axios'
import { useTranslation } from 'react-i18next'
import { getUserData } from "@utils"
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
const MySwal = withReactContent(Swal)

const first_config = {
  0: { title: 'Unverified', color: 'light-warning' },
  1: { title: 'Verified', color: 'light-success' }
}
const role_id_id = {
  2: { title: 'Network Admin', color: 'light-warning' },
  1: { title: 'Super Admin', color: 'light-success' }
}
// ** Avatar render function
const renderClient = row => {
  const stateNum = Math.floor(Math.random() * 6),
    states = ['light-success', 'light-danger', 'light-warning', 'light-info', 'light-primary', 'light-secondary'],
    color = states[stateNum]
  if (row.profile_photo !== null && row.profile_photo !== undefined) {
    return <Avatar className='mr-1' img={`${row.profile_photo}`} width='32' height='32' />
  } else {
    return <Avatar color={color || 'primary'} className='mr-1' content={row.first_name || ''} initials />
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
      axios.post("/disable-user-account", {
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
export const columns = ({t}) => {
  return [
  {
    name: t('First Name'),
    minWidth: '250px',
    selector: 'first_name',
    sortable: true,
    cell: row => (
      <div className='d-flex justify-content-left align-items-center'>
        {renderClient(row)}
        <div className='d-flex flex-column'>
          <span className='font-weight-bold'>{row.first_name} {row.last_name}</span>
          <small className='text-truncate text-muted mb-0'>{row.email}</small>
        </div>
      </div>
    )
  },
  {
    name: t('Email'),
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
  // {
  //   name: t('Role'),
  //   minWidth: '100px',
  //   selector: 'role_id_id',
  //   sortable: true,
  //   cell: row => {
  //     return (
  //       <Badge color={role_id_id[row.role_id_id].color} pill>
  //         {role_id_id[row.role_id_id].title}
  //       </Badge>
  //     )
  //   }
  // },
  {
    name: t('Phone'),
    selector: 'contact_number',
    sortable: true,
    minWidth: '100px',
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
    name: t('Verification Status'),
    minWidth: '100px',
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
    name: t('Account Active Status'),
    minWidth: '100px',
    selector: '',
    sortable: true,
    cell: row => <UserAccountStatusModal row={row} />
  },
  {
    name: t('Actions'),
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
}
// export default columns