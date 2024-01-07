// ================================================================================================
//  File Name: generateNewPassword.js
//  Description: Details of the Generate New Password.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useSkin } from '@hooks/useSkin'
import { Link, useParams, useHistory } from 'react-router-dom'
import { ChevronLeft } from 'react-feather'
import InputPassword from '@components/input-password-toggle'
import {
  Row, Col, CardTitle, CardText, Form, FormGroup, Label, Button,
  Spinner, CustomInput, Modal, ModalHeader, ModalBody, ModalFooter
} from 'reactstrap'
import '@styles/base/pages/page-auth.scss'
import { useState, Fragment } from "react"
import axios from '@axios'
import { toast, Slide } from 'react-toastify'
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import img2 from '@src/assets/images/logo/Logo4.png'

const MySwal = withReactContent(Swal)

const RememberMe = () => {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <Fragment>
      <span className='ml-25 text-primary' style={{ cursor: "pointer" }} onClick={() => setIsOpen(!isOpen)}>
        Terms & Conditions
      </span>

      <Modal
        isOpen={isOpen}
        toggle={() => setIsOpen(!isOpen)}
        className="modal-lg modal-dialog-scrollable"
      >
        <ModalHeader toggle={() => setIsOpen(!isOpen)} className="justify-content-center text-center">
          Terms & Conditions
        </ModalHeader>
        <ModalBody>
          <p>
            Please read this End-User License Agreement ("EULA") carefully before using the ZeroHack software (the "Software").
            By installing or using the Software, you agree to be bound by the terms and conditions of this EULA.
          </p>

          <h5>1. License Grant:</h5>
          <p className='ml-3'>
            a. Grant of License: WhizHack Technologies Pvt. Ltd. grants you a non-exclusive, non-transferable license to use the Software for your personal or business purposes, subject to the terms and conditions of this EULA.
            <br /><br />
            b. Scope of Use: You may use the Software on a single computer or device or, if applicable, in accordance with the number of licenses purchased. Unauthorized copying, distribution, or use of the Software is strictly prohibited.
            <br /><br />
            c. Updates and Support: WhizHack Technologies Pvt. Ltd. may provide updates and support for the Software at its discretion. This EULA applies to any such updates.
          </p>

          <h5>2. Restrictions:</h5>
          <p className='ml-3'>
            a. You may not:
            <br /><br />
            b. Reverse engineer, decompile, or disassemble the Software.
            <br /><br />
            c. Modify, adapt, translate, or create derivative works based on the Software.
            <br /><br />
            d. Remove or alter any copyright, trademark, or other proprietary notices from the Software.
            <br /><br />
            e. Use the Software for any illegal, harmful, or unethical purpose.
          </p>

          <h5>3. Ownership:</h5>
          <p className='ml-3'>a. WhizHack Technologies Pvt. Ltd. retains all rights, title, and interest in and to the Software, including all intellectual property rights.</p>

          <h5>4. Privacy:</h5>
          <p className='ml-3'>a. Use of the Software may require the collection and transmission of certain data, including personal information. By using the Software, you consent WhizHack Technologies Pvt. Ltd. collection and use of such data in accordance with <a href='https://whizhack.in/privacy-policy' target='_blank'> WhizHack Technologies Pvt. Ltd.</a></p>

          <h5>5. Termination:</h5>
          <p className='ml-3'>
            a. This EULA is effective until terminated by you or WhizHack Technologies Pvt. Ltd. You may terminate it at any time by uninstalling the Software and destroying all copies. WhizHack Technologies Pvt. Ltd. may terminate this EULA if you fail to comply with its terms and conditions. Upon termination, you must cease all use of the Software and destroy all copies.
          </p>

          <h5>6. Warranty Disclaimer:</h5>
          <p className='ml-3'>
            a. The Software is provided "as is" without warranties of any kind, either express or implied, including, but not limited to, the implied warranties of merchantability, fitness for a particular purpose, or non-infringement.
          </p>

          <h5>7. Limitation of Liability:</h5>
          <p className='ml-3'>
            a. To the fullest extent permitted by applicable law, WhizHack Technologies Pvt. Ltd. shall not be liable for any indirect, incidental, special, consequential, or punitive damages, or any loss of profits or revenues, whether incurred directly or indirectly, or any loss of data, use, goodwill, or other intangible losses, resulting from (i) your use or inability to use the Software or (ii) any unauthorized access to or use of the Software.
          </p>

          <h5>8. Governing Law:</h5>
          <p className='ml-3'>
            a. This EULA shall be governed by and construed in accordance with the laws of India. Any legal action arising out of or relating to this EULA shall be filed in the courts of Haryana and you hereby consent to the exclusive jurisdiction of such courts.
          </p>

          <h5>9. Entire Agreement:</h5>
          <p className='ml-3'>
            a. This EULA constitutes the entire agreement between you and WhizHack Technologies Pvt. Ltd. regarding the Software and supersedes all prior and contemporaneous agreements, representations, and understandings.
          </p>

          <p>
            By installing or using the Software, you acknowledge that you have read and understood this EULA and agree to be bound by its terms and conditions.
            <br />
            If you have any questions or concerns regarding this EULA, please contact WhizHack Technologies Pvt. Ltd. at <a href="mailto:support@whizhack.com">support@whizhack.com</a>
          </p>
        </ModalBody>
      </Modal>
    </Fragment>
  )
}

const GarnetNewPassword = () => {
  const [skin, setSkin] = useSkin()
  const [oldPassNotMatch, setOldPassNotMatch] = useState(null)
  const [confirmPass, setconfirmPass] = useState(null)
  const [loading, setLoading] = useState(false)
  const { id } = useParams()
  const history = useHistory()
  const illustration = skin === 'dark' ? 'reset-password-v2-dark.svg' : 'reset-password-v2.svg',
    source = require(`@src/assets/images/pages/${illustration}`).default

  const resetPasswordForm = (e) => {
    e.preventDefault()
    setLoading(true)
    const formData = new FormData(e.target)
    formData.append("u_id", id)
    if (e.target.new_password.value === e.target.confirm_password.value) {
      setconfirmPass(null)
      axios({
        url: "/generate-new-password",
        method: "post",
        data: formData
      }).then((res) => {
        setLoading(false)
        if (res.data.message_type === "success") {
          MySwal.fire({
            title: 'New Password Generated',
            text: 'Successfully updated  password, Please click the login button.',
            icon: 'success',
            customClass: {
              confirmButton: 'btn btn-primary'
            },
            buttonsStyling: false,
            confirmButtonText: 'Go Login'
          }).then(btnRes => {
            if (btnRes.isConfirmed) {
              history.push("/login")
            }
          })
        }


      }).catch((error) => {
        setLoading(false)
        const res = error.response.data
        if (res.message_type === "form_errror") {
          if (res.errors.non_field_errors[0] === "pass_not_match") {
            toast.error("Your old password and new password not match.", {
              position: "top-right",
              autoClose: 5000,
              hideProgressBar: false,
              closeOnClick: true,
              pauseOnHover: true,
              draggable: true,
              progress: undefined
            })
          }
          if (res.errors.non_field_errors[0] === "invalid_old_pass") {
            toast.error("Your old password is Invalid.", {
              position: "top-right",
              autoClose: 5000,
              hideProgressBar: false,
              closeOnClick: true,
              pauseOnHover: true,
              draggable: true,
              progress: undefined
            })
          }
          if (res.errors.non_field_errors[0] === "old_new_not_diff") {
            toast.error("Please enter different password of you old password.", {
              position: "top-right",
              autoClose: 5000,
              hideProgressBar: false,
              closeOnClick: true,
              pauseOnHover: true,
              draggable: true,
              progress: undefined
            })
          }
        }
      })
    } else {
      setLoading(false)
      setconfirmPass("Your confirmed password does not match.")
    }
  }

  return (
    <div className='auth-wrapper auth-v2'>
      <Row className='auth-inner m-0'>
        <Link className='brand-logo' to='/' onClick={e => e.preventDefault()}>
          <img src={img2} width="200px" height="50px" />
        </Link>
        <Col className='d-none d-lg-flex align-items-center p-5' lg='8' sm='12'>
          <div className='w-100 d-lg-flex align-items-center justify-content-center px-5'>
            <img className='img-fluid' src={source} alt='Login V2' />
          </div>
        </Col>
        <Col className='d-flex align-items-center auth-bg px-2 p-lg-5' lg='4' sm='12'>
          <Col className='px-xl-2 mx-auto' sm='8' md='6' lg='12'>
            <CardTitle tag='h2' className='font-weight-bold mb-1'>
              Generate New Password 🔒
            </CardTitle>
            <CardText className='mb-2'>Set your new passwords</CardText>
            <Form className='auth-reset-password-form mt-2' onSubmit={resetPasswordForm}>
              <FormGroup>
                <Label className='form-label' for='old-password' autoFocus>
                  Old Password
                </Label>
                <InputPassword className='input-group-merge' autoComplete="off" id='old-password' name="old_password" required />
                {oldPassNotMatch !== null ? <p className='text-danger m-1 p-0'>{oldPassNotMatch}</p> : ''}
              </FormGroup>
              <FormGroup>
                <Label className='form-label' for='new-password'>
                  New Password
                </Label>
                <InputPassword className='input-group-merge' autoComplete="off" id='new-password' name="new_password" required />
              </FormGroup>
              <FormGroup>
                <Label className='form-label' for='confirm-password'>
                  Confirm Password
                </Label>
                <InputPassword className='input-group-merge' autoComplete="off" id='confirm-password' name="confirm_password" required />
                {confirmPass !== null ? <p className='text-danger m-1 p-0'>{confirmPass}</p> : ''}
              </FormGroup>
              <FormGroup className="d-flex ">
                <CustomInput
                  type='checkbox'
                  required
                  className='custom-control-Primary'
                  id='remember-me'
                  label="I agree to"
                />
                <RememberMe />
              </FormGroup>
              {(loading === false) ? <Button.Ripple color='primary' block>Change Password </Button.Ripple> : <Button.Ripple type="button" color='primary' block disabled> <Spinner size="sm" />&nbsp;Checking... </Button.Ripple>}
            </Form>
            <p className='text-center mt-2'>
              <Link to='/login'>
                <ChevronLeft className='mr-25' size={14} />
                <span className='align-middle'>Back to login</span>
              </Link>
            </p>
          </Col>
        </Col>
      </Row>
    </div>
  )
}

export default GarnetNewPassword
