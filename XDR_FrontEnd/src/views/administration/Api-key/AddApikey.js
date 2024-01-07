// ================================================================================================
//  File Name: AddApiKey.js
//  Description: To Add Api key Details.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================


import React, { useState, Fragment } from 'react'
import { X } from 'react-feather'
import { Button, Modal, ModalHeader, ModalBody, Input, Label, Form, Spinner, Row, Col } from 'reactstrap'
import { useTranslation } from 'react-i18next'
import { useSelector } from 'react-redux'
import '@styles/react/libs/flatpickr/flatpickr.scss'
import axios from '@axios'
import { token, selectThemeColors } from '@utils'
import Swal from 'sweetalert2'
import Select from 'react-select'
import withReactContent from 'sweetalert2-react-content'
import api_msg from '../../../constants/api_message'
import { splitWord } from '../../../utility/helpers'

const AddNewModal = ({ open, handleModal, options }) => {
  const { t } = useTranslation()
  const MySwal = withReactContent(Swal)
  const [btnLoader, setBtnLoader] = useState(false)
  const [indiesData, setIndiesData] = useState([])
  const { env_trace, env_nids, env_hids } = useSelector((store) => store.pagesPermissions)

  //get product type from pagesPermissions coditions.
  const productTypes = []

  if (env_trace) {
    productTypes.push({ value: 'env_trace', label: 'TRACE', color: '#00B8D9', isFixed: true })
  }

  if (env_nids) {
    productTypes.push({ value: 'env_nids', label: 'NIDS', color: '#00B8D9', isFixed: true })
  }

  if (env_hids) {
    productTypes.push({ value: 'env_hids', label: 'HIDS', color: '#00B8D9', isFixed: true })
  }

  // const productInputHandle = (event) => {
  //   if (event !== null) {
  //     const eventMultipe = event.map((v) => v.value)
  //     axios
  //       .get(`/third-party-api-get-logindice?product_name=${eventMultipe.toString()}`, { headers: { Authorization: token() } })
  //       .then((res) => {
  //         if (res.data.message_type === 'success') {
  //           console.log(res.data)
  //           setIndiesData(res.data.indices)
  //         }
  //       })
  //   }
  // }

  const productInputHandle = (selectedOptions) => {
    if (selectedOptions !== null) {
      const selectedProducts = selectedOptions.map((option) => option.value)
  
      axios
        .get(`/third-party-api-get-logindice?product_name=${selectedProducts.toString()}`, { headers: { Authorization: token() } })
        .then((res) => {
          if (res.data.message_type === 'success') {
            const fetchedIndices = res.data.indices || [] // Ensure indices is an array
            setIndiesData(Array.isArray(fetchedIndices) ? fetchedIndices : [])
          }
        })
        .catch((error) => {
          // Handle error in fetching data
          console.error('Error fetching log indices:', error)
          setIndiesData([]) // Set indiesData to an empty array on error
        })
    } else {
      setIndiesData([]) // Set indiesData to an empty array if no selected options
    }
  }
  

  const formSubmitHandle = (event) => {
    event.preventDefault()
    setBtnLoader(true)

    // Gather form data
    const formData = new FormData(event.target)
    const apiType = formData.get('api_type')
    const logTypes = formData.getAll('log_type')
    const productTypes = formData.getAll('product_types')

    // Prepare the data to be sent in the POST request
    const postData = new FormData()
    postData.append('api_type', apiType)

    // Append each selected log type
    logTypes.forEach((type) => {
      postData.append('log_type[]', type)
    })
  
    // Append each selected product type
    productTypes.forEach((type) => {
      postData.append('product_types[]', type)
    })

    // Send the POST request using Axios
    axios
      .post('/updated-third-party-api-create-api-key', postData, { headers: { Authorization: token() } })
      .then((res) => {
        setBtnLoader(false)
        // Handle success response
        if (res.data.message_type === 'created') {
          MySwal.fire({
            title: api_msg.title_msg,
            text: 'Sit Back and Relax',
            icon: 'success',
            customClass: {
              confirmButton: 'btn btn-primary'
            },
            buttonsStyling: false
          }).then(() => {
            // Close the modal after success message is displayed
            handleModal()
          })
        } else if (res.data.message_type === 'form_errors') {
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
    <Modal isOpen={open} toggle={handleModal} className='sidebar-sm' modalClassName='modal-slide-in' contentClassName='pt-0'>
      <ModalHeader className='mb-3' toggle={handleModal} close={CloseBtn} tag='div'>
        <h5 className='modal-title'>{t('Create Api key')}</h5>
      </ModalHeader>
      <ModalBody className='flex-grow-1'>
        <Form onSubmit={formSubmitHandle}>
          <Row>
            <Col md='12'>
              <Label>API Type</Label>
              <Input type='select' name='api_type' required>
                <option value=''>Select...</option>
                <option value='1'>GET</option>
              </Input>
            </Col>
            <Col className='mb-1' md='12' sm='12'>
              <Label>Product Types</Label>
              <Select
                isMulti
                isClearable={false}
                theme={selectThemeColors}
                placeholder={<div className='select-placeholder-text' style={{ color: '#a5a7af' }}>Select...</div>}
                name='product_types'
                options={productTypes}
                className='react-select'
                classNamePrefix='select'
                onChange={productInputHandle}
                required={true}
              />
            </Col>
            <Col className='mb-1' md='12' sm='12'>
              <Label>Log Types</Label>
              <Select
                isMulti
                name='log_type'
                theme={selectThemeColors}
                isClearable={true}
                className='react-select'
                classNamePrefix='select'
                options={
                  indiesData.map((list) => ({
                    value: list,
                    label: splitWord(list),
                    color: '#00B8D9',
                    isFixed: true
                  }))
                }
              />
            </Col>
          </Row>
          {btnLoader === false ? (
            <Button.Ripple color='primary' className='btn-submit mr-1' type='submit'>
              {t('Create Api')}
            </Button.Ripple>
          ) : (
            <Button.Ripple color='success' className='btn-submit' type='submit' onClick={handleModal}>
              <Spinner size='sm' />
              &nbsp;{t('Creating Api')}...
            </Button.Ripple>
          )}
        </Form>
      </ModalBody>
    </Modal>
  )
}

export default AddNewModal