// ================================================================================================
//  File Name: AddNewModal.js
//  Description: Details of the Setting ( Billing ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** React Imports
import { useState } from 'react'
// ** Third Party Components
import { X } from 'react-feather'
import {
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  FormGroup,
  Input,
  Label,
  Form,
  Spinner
} from 'reactstrap'

// ** Styles
import '@styles/react/libs/flatpickr/flatpickr.scss'
import axios from '@axios'
import { token } from '@utils'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from "../../../constants/api_message"
const MySwal = withReactContent(Swal)
const AddNewModal = ({ open, handleModal }) => {
const [btnLoader, setBtnLoader] = useState(false) 

const url_link = "/addbilling/"
function submit_form(event) {
  setBtnLoader(true)
  event.preventDefault()
  
  const bodyFormData = new FormData(event.target)

  axios({
    method: "post",
    url: url_link,
    data: bodyFormData,
    headers : { Authorization: token()}
    
  })
    .then((res) => {
      setBtnLoader(false)
      if (res.data.message_type === "successfully_inserted") {
        MySwal.fire({
          title: api_msg.title_msg,
          text: 'Sit Back and Relax',
          icon: 'success',
          customClass: {
            confirmButton: 'btn btn-primary'
          },
          buttonsStyling: false
        })      

      } else if (res.data.message_type === "unsuccessful") {
          MySwal.fire({
            icon: 'error',
            title: api_msg.title_err,
            text: 'Something went wrong!',
            customClass: {
              confirmButton: 'btn btn-primary'
            },
           buttonsStyling: false
          })
        }
    })
    .catch((errors) => {
      setBtnLoader(false)
      MySwal.fire({
        icon: 'error',
        title: 'Oops!',
        text: 'Something went wrong!',
        customClass: {
          confirmButton: 'btn btn-primary'
        },
       buttonsStyling: false
      })
    })
}
  // ** Custom close btn
  const CloseBtn = <X className='cursor-pointer' size={15} onClick={handleModal} />

  return (
    <Modal
      isOpen={open}
      toggle={handleModal}
      className='sidebar-sm'
      modalClassName='modal-slide-in'
      contentClassName='pt-0'
    >
      <ModalHeader className='mb-3' toggle={handleModal} close={CloseBtn} tag='div'>
        <h5 className='modal-title'>Billings Details</h5>
      </ModalHeader>
      <ModalBody className='flex-grow-1'>
      <Form onSubmit={submit_form}>
      <FormGroup>
          <Label>
          Billing Name<span className='text-danger'>*</span>
          </Label>
          <Input
          type='text'
            name="billing_types"
            placeholder='Billing name'
          />
        </FormGroup>
        <FormGroup>
          <Label>
          Billing Description<span className='text-danger'>*</span>
          </Label>
          <Input
          type='textarea'
            name="billing_descriptions"
            placeholder='description'
          />
        </FormGroup>
        <FormGroup>
          <Label>
          Image<span className='text-danger'>*</span>
          </Label>
          <Input
          type='file'
            name="billing_image"

          />
        </FormGroup>
        {(btnLoader === false) ? <Button.Ripple color='primary' className='btn-submit mr-1' type='submit'> Submit </Button.Ripple> : <Button.Ripple color='success' className='btn-submit' type='submit'><Spinner size='sm' />&nbsp;Loading... </Button.Ripple>} 
        <Button color='secondary' onClick={handleModal} outline>
          Cancel
        </Button>
        </Form>
      </ModalBody>
    </Modal>
  )
}

export default AddNewModal