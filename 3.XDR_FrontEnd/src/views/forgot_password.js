// ================================================================================================
//  File Name: forget_password.js
//  Description: Details of the Forget password.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useSkin } from '@hooks/useSkin'
import { Link } from 'react-router-dom'
import { ChevronLeft } from 'react-feather'
import InputPassword from '@components/input-password-toggle'
import { Row, Col, CardTitle, CardText, Form, FormGroup, Input, Label, Button, Spinner, Badge } from 'reactstrap'
import '@styles/base/pages/page-auth.scss'
import { useState } from "react"
import axios from '@axios'
import { toast } from 'react-toastify'
import { useTranslation } from 'react-i18next'

import img2 from '@src/assets/images/logo/Logo4.png'
import { t } from 'i18next'

const PasswordComponent = ({otpMsgCheck, OtpResendHandle, resendOtp}) => {
  const inputs = document.querySelectorAll('#otp > *[id]')
  for (let i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener('keydown', function(event) {
      if (event.key === "Backspace") {
        inputs[i].value = ''
        if (i !== 0) inputs[i - 1].focus()
      } else {
        if (i === inputs.length - 1 && inputs[i].value !== '') {
          return true
        } else if (event.keyCode > 47 && event.keyCode < 58) {
          inputs[i].value = event.key
          if (i !== inputs.length - 1) inputs[i + 1].focus()
          event.preventDefault()
        } else if (event.keyCode > 64 && event.keyCode < 91) {
          inputs[i].value = String.fromCharCode(event.keyCode)
          if (i !== inputs.length - 1) inputs[i + 1].focus()
          event.preventDefault()
        }
      }
    })
  }
    return <>
            <p className='mt-1'>{t('Type your 6 digit security code')}</p>
            <div id="otp" className='mt-2 mb-2 auth-input-wrapper d-flex align-items-center justify-content-between'>
                <Input autoFocus maxLength='1' name='num_1' className='auth-input height-50 text-center numeral-mask mx-25 mb-1' type="text" id="first" />
                <Input maxLength='1' name='num_2' className='auth-input height-50 text-center numeral-mask mx-25 mb-1' type="text" id="second" />
                <Input maxLength='1' name='num_3' className='auth-input height-50 text-center numeral-mask mx-25 mb-1' type="text" id="third" />
                <Input maxLength='1' name='num_4' className='auth-input height-50 text-center numeral-mask mx-25 mb-1' type="text" id="fourth" />
                <Input maxLength='1' name='num_5' className='auth-input height-50 text-center numeral-mask mx-25 mb-1' type="text" id="fifth" />
                <Input maxLength='1' name='num_6' className='auth-input height-50 text-center numeral-mask mx-25 mb-1' type="text" id="sixth"/>
              </div> 
            {(otpMsgCheck) ? <p> <span className='text-danger'>{t("Enter all 6 digit of OTP")}</span> </p> : ""}
            <p className='text-right m-0'>
              <span>{t("Didn’t get the code?")}</span>
              {(!resendOtp) ? <span className='text-primary' style={{ cursor: "pointer" }} onClick={OtpResendHandle}>{t("Resend")}</span> : <Spinner size="sm" className='text-primary' />}
            </p>
            <FormGroup>
            <Label className='form-label' for='new-password'>
            {t("New Password")}
            </Label>
            <input type="hidden" name='action' value="RESET_PASS" />
            <InputPassword className='input-group-merge' autoComplete="off" id='new-password' name="new_password" pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*_=+-]).{8,16}$" required />
            </FormGroup>
            <FormGroup>
                <Label className='form-label' for='confirm-password'>{t("Confirm Password")}</Label>
                <InputPassword className='input-group-merge' autoComplete="off" id='confirm-password' name="confirm_password" pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*_=+-]).{8,16}$" required />
            </FormGroup>
        </>
}

const ForgotPassword = () => {
    const {t} = useTranslation()
    const [skin, setSkin] = useSkin()
    const [loading, setLoading] = useState(false)
    const illustration = skin === 'dark' ? 'reset-password-v2-dark.svg' : 'reset-password-v2.svg',
        source = require(`@src/assets/images/pages/${illustration}`).default

    const [optMsg, setOtpMsg] = useState("")
    const [otpCheck, setotpCheck] = useState(false)    
    const [otpMsgCheck, setOtpMsgCheck] = useState(false)
    const [emailId, setEmailId] = useState("")
    const [resendOtp, setResendOtp] = useState(false)


    const resetPasswordForm = (e) => {
        let mail_otp = NaN
        e.preventDefault()
        setEmailId(e.target.email.value)
        if (e.target.action.value !== undefined) {
        
            if (e.target.num_1.value === "" || e.target.num_2.value === "" || e.target.num_3.value === "" || e.target.num_4.value === "" || e.target.num_5.value === "" || e.target.num_6.value === "") {
                setOtpMsgCheck(true)
                return false
            }
          
            mail_otp = `${e.target.num_1.value}${e.target.num_2.value}${e.target.num_3.value}${e.target.num_4.value}${e.target.num_5.value}${e.target.num_6.value}`
              
            setOtpMsgCheck(false)
            
        }

        const formData = new FormData(e.target)
        formData.append("mail_otp", mail_otp)
        
        setLoading(true)
        axios({
            url: "/forgot-pass",
            method: "post",
            data: formData
        }).then((res) => {
            setLoading(false)

            if (res.data.message_type === "form_error") {
                if (res.data.errors !== undefined) {
                    if (res.data.errors.email !== undefined && res.data.errors.email[0] === "email_not_exist") {
                        toast.warn("Your email not exist please check your mail id.", {
                            position: "top-right",
                            autoClose: 5000,
                            hideProgressBar: false,
                            closeOnClick: true,
                            pauseOnHover: true,
                            draggable: true,
                            progress: undefined
                        })
                    }

                    if (res.data.errors.msg !== undefined && res.data.errors.msg[0] === "pass_not_match") {
                        setotpCheck(true)
                        setOtpMsg("Your old password & new password isn't matching.")
                    }

                    if (res.data.errors.msg !== undefined && res.data.errors.msg[0] === "otp_invalide") {
                        setotpCheck(true)
                        setOtpMsg("Invalid OTP.")                        
                    }
                }
            }

            if (res.data.message_type === "success") {               
                setotpCheck(true)
                setOtpMsg(<p>{t("Your password successfully reset, please login and continue")}<Link to="/">{t("Login")} </Link></p>)

                toast.success("Your password successfully reset, please log in.", {
                    position: "top-right",
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined
                    })
            }

            if (res.data.message_type === "otp_send_on_mail") {
                setotpCheck(true)
                setOtpMsg("OTP sent on email id, please check your emaill")
            }

        }).catch((error) => {
            setLoading(false)
        })

    }

    const OtpResendHandle = () => {
        if (emailId !== "") {
            setResendOtp(true)
            const fromDataOTP = new FormData()
            fromDataOTP.append("action", "FORGOT_RESEND")
            fromDataOTP.append("email", emailId)
            axios({
                url: "/resend-otp",
                method: "post",
                data:fromDataOTP
            }).then((res) => {
                setResendOtp(false)
                if (res.data.message_type === "otp_resend_on_mail") {
                    setotpCheck(true)
                    setOtpMsg("A new OTP has been sent to your mail address, please check your email.")
                }
            }).catch((error) => {
                setResendOtp(false)
            })
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
                        {t("Forgot Password")}🔒
                        </CardTitle>
                        <CardText className='mb-2'>{t("Please enter your email id to reset your password")}</CardText>
                        <Form className='auth-reset-password-form mt-2' onSubmit={resetPasswordForm}>
                            <FormGroup>
                                <Label for="email_id">{t("Email ID")}</Label>                                
                                <Input type="email" required  name="email" id="email_id" />
                            </FormGroup>

                            {(otpCheck) ? <PasswordComponent otpMsgCheck={otpMsgCheck} OtpResendHandle={OtpResendHandle} resendOtp={resendOtp} />  : ""}

                            <Badge color='warning' className='badge-glow'>
                            {(optMsg !== "") ? optMsg : ""}
                          </Badge> 
                          <div className='mt-1'>
                            {(loading === false) ? <Button.Ripple color='primary' block>{t("Submit")}</Button.Ripple> : <Button.Ripple type="button" color='primary' block disabled> <Spinner size="sm" />&nbsp;{t("Checking")}...</Button.Ripple>}
                            </div>
                        </Form>
                        <p className='text-center mt-2'>
                            <Link to='/login'>
                                <ChevronLeft className='mr-25' size={14} />
                                <span className='align-middle'>{t("Back to login")}</span>
                            </Link>
                        </p>
                    </Col>
                </Col>
            </Row>
        </div>
    )
}

export default ForgotPassword
