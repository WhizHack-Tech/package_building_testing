// ================================================================================================
//  File Name: AddNewModal.js
//  Description: Details of the Administration ( List User Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
// ** React Imports
import { useState, useEffect, useRef } from 'react'
import { AvForm, AvInput, AvGroup, AvFeedback } from 'availity-reactstrap-validation-safe'
// ** Third Party Components
import { X } from 'react-feather'

// ** Utils
import { token } from '@utils'
import axios from '@axios'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

import {
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  FormGroup,
  Label,
  FormText,
  Spinner,
  Input
} from 'reactstrap'

import { clientAllData } from "../store/action/index"

import '@styles/react/libs/flatpickr/flatpickr.scss'
import api_msg from "../../../../constants/api_message"
import { useDispatch } from 'react-redux'

const AddNewModal = ({ open, handleModal }) => {
  const MySwal = withReactContent(Swal)
  const [btnLoader, setBtnLoader] = useState(false)
  const [countrys, setCountrys] = useState([])
  const [orgData, setOrgData] = useState([{ value: null, label: null }])
  const [locationData, setLocationData] = useState([])
  const [optOfLocation, setOptOfLocation] = useState([])
  const dispatch = useDispatch()

  const validateContact = (value) => {
    if (!value) return false // Field is required; validation handled by 'required' attribute
    // Remove non-digit characters (e.g., parentheses and spaces) and check the length
    return value.replace(/\D/g, '').length === 10
  }

  useEffect(() => {

    axios
      .get(`/countrydata/`, { headers: { Authorization: token() } })
      .then((res) => {
        if (res.data.message_type === "data_found") {
          setCountrys(res.data.data)
        }
      })
      .catch((error) => {
        console.error('Failed to fetch country data:', error.message)
      })

    axios.get('/location-data-org', { headers: { Authorization: token() } })
      .then((res) => {
        if (res.data.message_type === "data_found") {
          const orgList = []
          const orgLocationList = []
          if (res.data.data.length > 0) {
            res.data.data.forEach((element, index) => {
              orgList[index] = { value: element.organization_id, label: `${element.organization_name}` }
              orgLocationList[element.organization_id] = element.location

            })
          }

          setLocationData(orgLocationList)
          setOrgData(orgList)
        }
      })
      .catch((error) => {
        console.error('Failed to fetch country data:', error.message)
      })

  }, [])


  const [data, setData] = useState({
    organization_id: '',
    first_name: '',
    last_name: '',
    email: '',
    country: '',
    contact_number: '',
    user_role_id: '',
    location_id: ''
  })

  function submit(e) {
    setBtnLoader(true)
    e.preventDefault()
    axios.post("/usertodb", {
      organization_id: data.organization_id,
      first_name: data.first_name,
      last_name: data.last_name,
      email: data.email,
      country: data.country,
      contact_number: data.contact_number,
      role_id: data.user_role_id,
      location_id: data.location_id

    }, { headers: { Authorization: token() } })
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
          }).then(btnRes => {
            if (btnRes.isConfirmed) {
              dispatch(clientAllData())
            }
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
        const er = errors.response.data
        if (er.message_type === "unsuccessful") {
          if (er.errors.email !== undefined && er.errors.email['0'] !== "") {
            MySwal.fire({
              icon: 'error',
              title: 'Oops!',
              text: er.errors.email['0'],
              customClass: {
                confirmButton: 'btn btn-primary'
              },
              buttonsStyling: false
            })
          } else {
            MySwal.fire({
              icon: 'error',
              title: 'Oops!',
              text: "Something went wrong!",
              customClass: {
                confirmButton: 'btn btn-primary'
              },
              buttonsStyling: false
            })
          }
        }
      })
  }

  function handle(e) {
    const newdata = { ...data }
    newdata[e.target.id] = e.target.value
    setData(newdata)
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
      <ModalHeader className='mb-1' toggle={handleModal} close={CloseBtn} tag='div'>
        <h5 className='modal-title'>User Config Details</h5>
      </ModalHeader>
      <ModalBody className='flex-grow-1'>
        <AvForm onSubmit={(e) => submit(e)}>
          <FormGroup>
            <Label for="organization_id">Organization Name</Label>
            <Input type='select' name='organization_id' id='organization_id' onChange={(e) => {
              handle(e)
              setOptOfLocation(locationData[e.target.value])
            }}>
              <option disabled selected={true}>--Select Organization Name--</option>
              {(orgData) ? orgData.map((row, key) => (<option key={key} value={row.value}>{row.label}</option>)) : null}
            </Input>
          </FormGroup>
          <FormGroup>
            <Label for="location_type">Location</Label>
            <Input type='select' name='location_id' id='location_id' onChange={(e) => handle(e)}>
              <option disabled selected={true}>--Select Location--</option>
              {(optOfLocation) ? optOfLocation.map((row, key) => (<option key={key} value={row.id}>{row.city} ({row.branchcode}) </option>)) : null}

            </Input>
          </FormGroup>
          <FormGroup>
            <Label for='full-name'>First Name</Label>
            <AvInput name='first_name' id='first_name' placeholder='first name' onChange={(e) => handle(e)} required />
          </FormGroup>
          <FormGroup>
            <Label for='full-name'>Last Name</Label>
            <AvInput name='last_name' id='last_name' placeholder='last name' onChange={(e) => handle(e)} required />
          </FormGroup>
          <FormGroup>
            <Label for='email'>Email</Label>
            <AvInput type='email' name='email' id='email' placeholder='email' onChange={(e) => handle(e)} required />
            <FormText color='muted'>You can use letters, numbers & periods</FormText>
          </FormGroup>
          <FormGroup>
            <Label>Country</Label>
            <select className="form-control" onChange={(e) => handle(e)} name='country' id='country' required>
              <option value="0">--Select Country--</option>
              {countrys.map((values, key) => (
                <option key={key} value={values.id}>
                  {values.country_name}
                </option>
              ))}
            </select>
          </FormGroup>
          <AvGroup>
            <Label for='contact'>Contact</Label>
            <AvInput
              name='contact_number'
              id='contact_number'
              placeholder='(+91) 9732212158'
              onChange={handle}
              validate={{ custom: validateContact }}
              required
            />
            <AvFeedback>This field is required.</AvFeedback>
            <AvFeedback>Contact should have exactly 10 digits.</AvFeedback>
          </AvGroup>
          <FormGroup>
            <Label for='user-role'>User Role</Label>
            <AvInput type='select' id='user_role_id' name='user_role-id' onChange={(e) => handle(e)} required>
              <option value='0'>---Select Role---</option>
              <option value='1'>Super Admin</option>
              {/* <option value='2'>Network Admin</option>        */}
            </AvInput>
          </FormGroup>
          {(btnLoader === false) ? <Button.Ripple color='primary' className='btn-submit mr-1' type='submit'> Submit </Button.Ripple> : <Button.Ripple color='success' className='btn-submit' type='submit'><Spinner size='sm' />&nbsp;Loading... </Button.Ripple>}
          <Button type='reset' color='secondary' outline onClick={handleModal}>
            Cancel
          </Button>
        </AvForm>
      </ModalBody>
    </Modal>
  )
}

export default AddNewModal