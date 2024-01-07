// ================================================================================================
//  File Name: AddApiKey.js
//  Description: To Add Api key Details.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================

import { X } from 'react-feather'
import { useState, useEffect } from 'react'
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
import { useTranslation } from 'react-i18next'
// ** Styles
import '@styles/react/libs/flatpickr/flatpickr.scss'
import axios from '@axios'
import { token } from '@utils'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from "../../../constants/api_message"

const AddNewModal = ({ open, handleModal }) => {
  const { t } = useTranslation()
  const MySwal = withReactContent(Swal)
  const [btnLoader, setBtnLoader] = useState(false)

  const [application, setapplication] = useState([])

  useEffect(() => {
    axios.get(`/application-views`, {
      headers: { Authorization: token() }
    }).then((res) => {
      setapplication(res.data)
    })
  }, [])

  const formSubmitHandle = (event) => {
    setBtnLoader(true)
    event.preventDefault()
    axios.post("/create-api-keys", {
      api_type: event.target.api_type.value,
      application_id: event.target.application_id.value
    }, { headers: { Authorization: token() } })
      .then((res) => {
        setBtnLoader(false)
        if (res.data.message_type === "created") {
          MySwal.fire({
            title: api_msg.title_msg,
            text: 'Sit Back and Relax',
            icon: 'success',
            customClass: {
              confirmButton: 'btn btn-primary'
            },
            buttonsStyling: false
          })

        } else if (res.data.message_type === "form_errors") {
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
        <h5 className='modal-title'>{t('Create Api key')}</h5>
      </ModalHeader>
      <ModalBody className='flex-grow-1'>
        <Form onSubmit={formSubmitHandle}>
          <FormGroup>
            <Label for='application_id'>{t('Select application')}</Label>
            <select className="form-control" name='application_id' id='application_id' required>
              <option value="" disabled selected>--Select--</option>
              {application.map((values, key) => (
                <option key={key} value={values.id}>
                  {values.application_name}
                </option>
              ))}
            </select>
          </FormGroup>
          <FormGroup>
            <Label for='api_type'>{t('API Type')}</Label>
            <Input type='select' id='api_type' name='api_type'>
              <option value='' disabled selected >---Select---</option>
              <option value='Full-control'>Full Control</option>
              {/* <option value='Modify'>Modify</option>
              <option value='Read-only'>Read Only</option>
              <option value='Read-Write'>Read Write</option> */}
            </Input>
          </FormGroup>
          {(btnLoader === false) ? <Button.Ripple color='primary' className='btn-submit mr-1' type='submit'>{t('Create Api')}</Button.Ripple> : <Button.Ripple color='success' className='btn-submit' type='submit' onClick={handleModal}><Spinner size='sm' />&nbsp;{t('Creating Api')}...</Button.Ripple>}
        </Form>
      </ModalBody>
    </Modal>
  )
}

export default AddNewModal