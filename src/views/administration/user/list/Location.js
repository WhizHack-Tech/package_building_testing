// ================================================================================================
//  File Name: Location.js
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
    Col,
    Label,
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
import {
    AvForm,
    AvGroup,
    AvInput,
    AvFeedback
} from 'availity-reactstrap-validation-safe'
const Location = ({ open, handleModal1 }) => {
    const dispatch = useDispatch()
    const store = useSelector(state => state.users)

    // useEffect(() => {
    //     dispatch(getAllData())
    // }, [])
    const [btnLoader, setBtnLoader] = useState(false)
    // ## timezone Api
    const [timezone, setTimezone] = useState([])
    const [zoneType, setZoneType] = useState("")
    const [timezone_id, setTimezone_id] = useState('')
    useEffect(() => {
        axios.get(`/timezonedata/`, { headers: { Authorization: token() } }).then((res) => {
            setTimezone(res.data)
        })
    }, [])

    const zoneHandle = () => {
        setTimezone_id($("#time_zone option:selected").val())
        setZoneType($("#time_zone option:selected").data("zone"))
    }

    // ## Country Api
    const [country, setCountry] = useState([])
    useEffect(() => {
        axios.get(`/countrydata/`, { headers: { Authorization: token() } }).then((res) => {
            setCountry(res.data)
        })
    }, [])

    //## Plan Api
    const [plan, setPlan] = useState([])
    useEffect(() => {
        axios.get(`/planlist/`, { headers: { Authorization: token() } }).then((res) => {
            setPlan(res.data)
        })
    }, [])
    // ## Billing Api
    const [billing, setBilling] = useState([])
    useEffect(() => {
        axios.get(`/billinglist/`, { headers: { Authorization: token() } }).then((res) => {
            setBilling(res.data)
        })
    }, [])
    // ** POst api
    const url_link = "/location-org"
    function submit_form(event) {
        setBtnLoader(true)
        event.preventDefault()

        const bodyFormData = new FormData(event.target)

        axios({
            method: "post",
            url: url_link,
            data: bodyFormData,
            headers: { Authorization: token() }

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
    const CloseBtn = <X className='cursor-pointer' size={15} onClick={handleModal1} />

    return (
        <Modal
            isOpen={open}
            toggle={handleModal1}
            className='sidebar-sm'
            modalClassName='modal-slide-in'
            contentClassName='pt-0'
        >
            <ModalHeader className='mb-3' toggle={handleModal1} close={CloseBtn} tag='div'>
                <h5 className='modal-title'>Attach Location Details</h5>
            </ModalHeader>
            <ModalBody className='flex-grow-1'>
                <div className='content-header'>
                    <h5>Organization Details</h5>
                    <small className='text-muted'>Enter Your  Organization Details.</small>
                </div>
                <Col sm={24}>
                    <hr />
                </Col>
                <AvForm onSubmit={submit_form}>
                    <FormGroup>
                        <Label for='user-role'>Organization Name</Label>
                        <select className="form-control Col-md-3" name='org_id' id="organization_type" required>
                            <option>--Select user--</option>
                            {store.data.map((value, key) => (
                                <option key={key} value={value.org_id}>
                                    {value.organization_name}
                                </option>
                            ))}
                        </select>
                    </FormGroup>
                    <AvGroup>
                        <Label className='form-label'>
                            Email
                        </Label>
                        <AvInput type='text' name='email' />
                        <AvFeedback>Please enter a valid Email!</AvFeedback>
                    </AvGroup>
                    <div className='content-header'>
                        <h5>Address Details</h5>
                        <small className='text-muted'>Enter Your Address Details.</small>
                    </div>
                    <Col sm={24}>
                        <hr />
                    </Col>
                    <AvGroup>
                        <Label className='form-label'>
                            Address
                        </Label>
                        <AvInput type='text' name='address' />
                        <AvFeedback>Please enter a valid Address!</AvFeedback>
                    </AvGroup>
                    <AvGroup>
                        <Label className='form-label'>
                            Phone Number
                        </Label>
                        <AvInput type='text' name='phone_number' />
                        <AvFeedback>Please enter a valid Phone Number!</AvFeedback>
                    </AvGroup>
                    <AvGroup>
                        <Label className='form-label'>
                            Branch Code
                        </Label>
                        <AvInput type='text' name='branchcode' />
                        <AvFeedback>Please enter a valid Branch Code!</AvFeedback>
                    </AvGroup>
                    <AvGroup>
                        <Label className='form-label'>
                            City
                        </Label>
                        <AvInput type='text' name='city' />
                        <AvFeedback>Please enter a valid City!</AvFeedback>
                    </AvGroup>
                    <AvGroup>
                        <Label className='form-label'>
                            State/Region
                        </Label>
                        <AvInput type='text' name='state' />
                        <AvFeedback>Please enter a valid State/Region!</AvFeedback>
                    </AvGroup>
                    <AvGroup>
                        <Label>Country</Label>
                        <select className="form-control" name='country_id'>
                            <option value="0">--Select Country--</option>
                            {country.map((values, key) => (
                                <option key={key} value={values.id}>
                                    {values.country_name}
                                </option>
                            ))}
                        </select>
                    </AvGroup>
                    <AvGroup>
                        <Label className='form-label'>
                            pincode
                        </Label>
                        <AvInput type='text' name='pincode' />
                        <AvFeedback>Please enter a valid pincode!</AvFeedback>
                    </AvGroup>
                    <AvGroup>
                        <Label>Timezone</Label>
                        <select className="form-control" name='timezone_id' onChange={zoneHandle} id='time_zone' >
                            <option value="0">--Select Timezone--</option>
                            {timezone.map((values, key) => (
                                <option key={key} value={values.id} data-zone={values.GMT_Offset}>
                                    {values.Time_Zone}
                                </option>
                            ))}
                        </select>
                    </AvGroup>
                    <AvGroup>
                        <Label className='form-label'>
                            Zone
                        </Label>
                        <AvInput type='text' name="timezone" value={zoneType} disabled />
                    </AvGroup>
                    <AvGroup>
                        <Label className='form-label'>
                            Fax Number
                        </Label>
                        <AvInput type='text' name='fax_number' />
                        <AvFeedback>Please enter a valid Fax!</AvFeedback>
                    </AvGroup>
                    <AvGroup>
                        <Label className='form-label'>
                            GST Number
                        </Label>
                        <AvInput type='text' name='gst_id' />
                        <AvFeedback>Please enter a valid Gst!</AvFeedback>
                    </AvGroup>
                    <AvGroup>
                        <Label className='form-label'>
                            TAN Number
                        </Label>
                        <AvInput type='text' name='tan_id' />
                        <AvFeedback>Please enter a valid TAN!</AvFeedback>
                    </AvGroup>
                    <AvGroup>
                        <Label className='form-label'>
                            PAN Number
                        </Label>
                        <AvInput type='text' name='pan_id' />
                        <AvFeedback>Please enter a valid PAN!</AvFeedback>
                    </AvGroup>
                    <AvGroup>
                        <Label className='form-label'>
                            CIN Number
                        </Label>
                        <AvInput type='text' name='cin_id' />
                        <AvFeedback>Please enter a valid CIN!</AvFeedback>
                    </AvGroup>
                    <AvGroup>
                        <Label>GST Image</Label>
                        <AvInput type='file' name="gst_image" />
                    </AvGroup>
                    <AvGroup>
                        <Label>TAN Image</Label>
                        <AvInput type='file' name="tan_image" />
                    </AvGroup>
                    <AvGroup>
                        <Label>PAN Image</Label>
                        <AvInput type='file' name="pan_image" />
                    </AvGroup>
                    <AvGroup>
                        <Label>CIN Image</Label>
                        <AvInput type='file' name="cin_image" />
                    </AvGroup>
                    <div className='content-header'>
                        <h5>Plan Details</h5>
                        <small className='text-muted'>Enter Your Plan Details.</small>
                    </div>
                    <Col sm={24}>
                        <hr />
                    </Col>
                    <AvGroup>
                        <Label>Plan</Label>
                        <select className="form-control" name='plan_id' id='plan_id' required>
                            <option value="0">--Select user--</option>
                            {plan.map((values, key) => (
                                <option key={key} value={values.id}>
                                    {values.plan_name}
                                </option>
                            ))}
                        </select>
                    </AvGroup>
                    <AvGroup>
                        <Label>Billing</Label>
                        <select className="form-control" name='billing_id' id='blling_id' required>
                            <option value="0">--Select user--</option>
                            {billing.map((values, key) => (
                                <option key={key} value={values.id}>
                                    {values.billing_types}
                                </option>
                            ))}
                            <AvFeedback>You must agree to our Terms & Conditions</AvFeedback>
                        </select>
                    </AvGroup>
                    <div className='content-header'>
                        <h5>Type Of Service</h5>
                        <small className='text-muted'>Enter Your Customer Type Details.</small>
                    </div>
                    <Col sm={12}>
                        <hr />
                    </Col>
                    <AvGroup>
                        <Label>Customer Type</Label>
                        <AvInput type='select' id='customer_types' name="customer_types">
                            <option value='' disabled selected>...Select...</option>
                            <option value='1'>New</option>
                            <option value='2'>Returning</option>
                            <option value='3'>Referrals</option>
                        </AvInput>
                    </AvGroup>
                    <AvGroup>
                        <Label>Environment Type</Label>
                        <AvInput type='select' name="environment_type">
                            <option value='' disabled selected>...Select...</option>
                            <option value='1'>Self Manage</option>
                            <option value='2'>Admin Manage</option>
                        </AvInput>
                    </AvGroup>
                    {(btnLoader === false) ? <Button.Ripple color='primary' className='btn-submit mr-1' type='submit'> Submit </Button.Ripple> : <Button.Ripple color='success' className='btn-submit' type='submit'><Spinner size='sm' />&nbsp;Loading... </Button.Ripple>}
                    <Button type='reset' color='secondary' outline onClick={handleModal1}>
                        Cancel
                    </Button>
                </AvForm>
            </ModalBody>
        </Modal>
    )
}

export default Location