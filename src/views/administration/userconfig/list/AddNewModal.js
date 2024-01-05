// ================================================================================================
//  File Name:  AddNewModal.js
//  Description: User Config Details.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================
// ** React Imports
import { useState, useEffect, useRef } from 'react'
import { AvForm, AvInput } from 'availity-reactstrap-validation-safe'
// ** Third Party Components
import { X } from 'react-feather'
import { useTranslation } from 'react-i18next'
// ** Utils
import { token } from '@utils'
import {
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  FormGroup,
  Label,
  FormText,
  Spinner
} from 'reactstrap'

// ** Styles
import '@styles/react/libs/flatpickr/flatpickr.scss'
import axios from '@axios'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from "../../../../constants/api_message"
const AddNewModal = ({ open, handleModal }) => {
  const {t} = useTranslation()
  // ** States
  const MySwal = withReactContent(Swal)
  const [btnLoader, setBtnLoader] = useState(false)
  const [countrys, setCountrys] = useState([])
// ** Axios Api for country list 
  useEffect(() => {
    axios.get(`/countries`, { headers: { Authorization: token() } }).then((res) => {
      setCountrys(res.data)
    })
  }, [])

// ** Axios Api for user config details  
  function formSubmitHandle(e, errors) {
    e.preventDefault()
    const fromData = new FormData(e.target)
    if (errors && !errors.length) {
        setBtnLoader(true)
      axios("/user-register", {
        method:"post",
        data:fromData,
        headers: { Authorization: token() }
      })
        .then((res) => {
          setBtnLoader(false)
            if (res.data.message_type === "sub_client_created") {
              MySwal.fire({
                title: api_msg.title_msg,
                text: 'Sit Back and Relax',
                icon: 'success',
                customClass: {
                  confirmButton: 'btn btn-primary'
                },
                buttonsStyling: false
              }).then(btnRes => {
                if (btnRes.isConfirmed) {
                  // dispatch(clientAllData())
                }
              })
        
            } else if (res.data.message_type === "s_is_w") {
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
          const data = errors.response
          
          if (data.data.message_type !== undefined && data.data.message_type === "form_error") {
            if (data.data.errors.email === "already_exists") {
              MySwal.fire({
                icon: 'warning',
                title: 'Oops!',
                text: 'This email Id already exists.',
                customClass: {
                  confirmButton: 'btn btn-primary'
                },
                buttonsStyling: false
              })
            }
            
          } else {
            MySwal.fire({
              icon: 'error',
              title: 'Oops!',
              text: `Something went wrong! with ${errors.name}`,
              customClass: {
                confirmButton: 'btn btn-primary'
              },
              buttonsStyling: false
            })
          }          
        })
    }
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
        <h5 className='modal-title'>{t('User Config Details')}</h5>
      </ModalHeader>
      <ModalBody className='flex-grow-1'>
        <AvForm onSubmit={formSubmitHandle}>
          <FormGroup>
            <Label for='full-name'>{t('First Name')}</Label>
            <AvInput name='first_name' id='first_name' placeholder={t('First Name')} required />
          </FormGroup>
          <FormGroup>
            <Label for='full-name'>{t('Last Name')}</Label>
            <AvInput name='last_name' id='last_name' placeholder={t('Last Name')} required />
          </FormGroup>
          <FormGroup>
            <Label for='email'>{t('Email')}</Label>
            <AvInput type='email' name='email' id='email' placeholder={t('Email')} required />
            {/* <FormText color='muted'>You can use letters, numbers & periods</FormText> */}
          </FormGroup>
          <FormGroup>
            <Label>{t('Country')}</Label>
            <select className="form-control" name='country' id='country' required>
              <option value="0">--Select Country--</option>
              {countrys.map((values, key) => (
                <option key={key} value={values.id}>
                  {values.country_name}
                </option>
              ))}
            </select>
          </FormGroup>
          <FormGroup>
            <Label for='contact'>{t('Contact')}</Label>
            <AvInput name='contact_number' id='contact_number' placeholder='(+91) 8447223249' required />
          </FormGroup>
          <FormGroup>
            <Label for='user-role'>{t('User Role')}</Label>
            <AvInput type='select' id='role_id' name='role_id' required>
              <option value='0'>---Select Role---</option>
              <option value='1'>Super Admin</option>
              {/* <option value='2'>Network Admin</option> */}
            </AvInput>
          </FormGroup>
          {(btnLoader === false) ? <Button.Ripple color='primary' className='btn-submit mr-1' type='submit'>{t('Submit')} </Button.Ripple> : <Button.Ripple color='success' className='btn-submit' type='submit'><Spinner size='sm' />&nbsp;{t('Loading')}...</Button.Ripple>}

        </AvForm>
      </ModalBody>
    </Modal>
  )
}

export default AddNewModal