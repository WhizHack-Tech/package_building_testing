// ================================================================================================
//  File Name: data.js
//  Description: Details of the Setting ( Application ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** Custom Components
import Avatar from '@components/avatar'
import { Link } from 'react-router-dom'
// ** Third Party Components
import { Eye } from 'react-feather'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import { useState } from 'react'
import { getUserData } from "@utils"
import axios from '@axios'
import InputPasswordToggle from '@components/input-password-toggle'
import { Badge, CustomInput, Modal, ModalHeader, ModalBody, FormGroup, ModalFooter, Button, Spinner } from 'reactstrap'
import { format } from 'date-fns'
const MySwal = withReactContent(Swal)

// ** Renders Client Columns
const renderClient = row => {
  const stateNum = Math.floor(Math.random() * 6),
    states = ['light-success', 'light-danger', 'light-warning', 'light-info', 'light-primary', 'light-secondary'],
    color = states[stateNum]

  if (row.billing_image) {
    return <Avatar className='mr-1' img={row.billing_image} width='32' height='32' />
  } else {
    return <Avatar color={color || 'primary'} className='mr-1' content={row.billing_types || 'John Doe'} initials />
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
      axios.post("change-application-status", {
        id: row.id,
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
    name: 'Application name',
    selector: 'application_name',
    sortable: true,
    minWidth: '100px'
  },
  {
    name: 'Description',
    selector: 'application_descriptions',
    sortable: true,
    minWidth: '150px'
  },
  {
    name: 'Date',
    selector: 'created_at',
    sortable: true,
    minWidth: '100px',
    cell: row => {
      return (
        <div className='d-flex justify-content-left align-items-center'>
          <Badge color='light-primary'>
          <span className='font-weight-bold text-uppercase'>{format(new Date(row.created_at), "yyyy-MM-dd, h:mm:ss a")}</span>
          </Badge>
        </div>
      )
    }
  },
  {
    name: 'Account Active Status',
    minWidth: '50px',
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
        <Link to={`/settings/editapplication/${row.id}`} id={`pw-tooltip-${row.id}`}>
          <Eye size={17} className='mx-1' />
        </Link>
      </div>
    )
  }
]

export default columns