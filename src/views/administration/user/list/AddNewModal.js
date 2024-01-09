// ================================================================================================
//  File Name: AddNewModal.js
//  Description: Details of the Administration ( Add Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
// ** React Imports
import { useState, useEffect } from 'react'
import $ from 'jquery'
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
import { useDispatch, useSelector } from 'react-redux'
import { getAllData } from '../store/action'
// ** Utils
import { token } from '@utils'
// ** Styles
import '@styles/react/libs/flatpickr/flatpickr.scss'
import axios from '@axios'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import api_msg from "../../../../constants/api_message"
const MySwal = withReactContent(Swal)
const AddNewModal = ({ open, handleModal }) => {
  let locationRowData = new Map()
  const dispatch = useDispatch()
  const store = useSelector(state => state.users)

  const [btnLoader, setBtnLoader] = useState(false)
  const [locationData, setLoactionData] = useState([])

  useEffect(() => {
    dispatch(getAllData())
  }, [])

  if (store.loading === true) {
    locationRowData.clear()
    store.data.forEach(value => {
      if (value.location !== undefined && value.location !== null) {
        locationRowData.set(value.organization_id, [value.location][0])
      }
    })   
  }

  const rand_num = (length) => {
    let result = ''
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    const charactersLength = characters.length
    for (let i = 0; i < length; i++) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength))
    }
    return result
  }

  const form_attach_agent = (event) => {
    setBtnLoader(true)
    event.preventDefault()
    const locationID = $("#location_type option:selected").data("locationid")
    const sensorName = event.target.location_type.value
    const agent_network = `xdr-network-map-${sensorName}`
    const agent_str = `xdr-logs-${sensorName}`
    const wazuhlogs_str = `xdr-wazuhlogs-${sensorName}`
    const trace_str = `xdr-trace-${sensorName}`

    axios.post(`/agentintodb`, {
      organization_id: event.target.organization_id.value,
      attach_agent_group: agent_str.toString(),
      attach_agent_network: agent_network.toString(),
      wazuh_attach_agent: wazuhlogs_str.toString(),
      trace_attach_agent: trace_str.toString(),
      db_username: event.target.dbusername.value,
      db_password: event.target.dbpassword.value,
      org_location: locationID,
      attach_agent_key: `${rand_num(4)}-${rand_num(4)}-${rand_num(4)}-${rand_num(4)}`
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
          })

        } else if (res.data.message_type === "unsuccessful") {
          MySwal.fire({
            icon: 'error',
            title: 'Oops...',
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

  const orgListHandle = (event) => {
    if (locationRowData.size > 0) {
      setLoactionData(locationRowData.get(event.target.value))
    }
  }

  const LoactionOptionList = () => {
    if (locationData !== undefined && locationData.length > 0) {
      return locationData.map((value, key) => (      
        <option key={key} value={value.org_name} data-locationid={value.id}>
          {value.city}-{value.branchcode}
        </option>
      ))
    }

    return null
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
        <h5 className='modal-title'>Attach Agent Details</h5>
      </ModalHeader>
      <ModalBody className='flex-grow-1'>
        <Form onSubmit={form_attach_agent}>
          <FormGroup>
            <Label for="organization_id">Organization Name</Label>
            <Input type='select' name='organization_id' id='organization_id' onChange={orgListHandle}>
              <option disabled selected={true}>--Select Organization Name--</option>
              {(store.loading === true) ? store.data.map((value, key) => (<option key={key} value={value.organization_id}>{value.organization_name}</option>)) : null}
            </Input>
          </FormGroup>
          <FormGroup>
            <Label for="location_type">Location</Label>
            <Input type='select' name='location_type' id='location_type'>
              <option disabled selected={true}>--Select Location--</option>
              <LoactionOptionList />
            </Input>
          </FormGroup>
          <FormGroup>
            <Label for="useName" className='form-label'>
              Database Username
            </Label>
            <Input type='text' id="useName" name="dbusername" />
          </FormGroup>
          <FormGroup>
            <Label for="passText" className='form-label'>
              Database Password
            </Label>
            <Input autoComplete="off" id="passText" type='password' name="dbpassword" />
          </FormGroup>
          {(btnLoader === false) ? <Button.Ripple color='primary' className='btn-submit mr-1' type='submit'> Submit </Button.Ripple> : <Button.Ripple color='success' className='btn-submit' disabled type='button'><Spinner size='sm' />&nbsp;Loading... </Button.Ripple>}
          <Button type='reset' color='secondary' outline onClick={handleModal}>
            Cancel
          </Button>
        </Form>
      </ModalBody>
    </Modal>
  )
}

export default AddNewModal