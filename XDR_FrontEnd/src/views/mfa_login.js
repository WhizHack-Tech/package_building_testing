// ================================================================================================
//  File Name: maf_login.js
//  Description: Details of the Multi Factor Authucation.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** React Imports
import { Link, useParams, useHistory } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import OTPInput from "otp-input-react"
// ** Reactstrap Imports
import { Row, Col, CardTitle, CardText, Button, Form, Spinner, Badge } from 'reactstrap'
// ** Import CSSStyles
import '@styles/base/pages/page-authentication.scss'
// ** Import Image
import img2 from '@src/assets/images/logo/Logo4.png'
import axios from "@axios"
import { useState, useContext, Fragment } from 'react'
import { toast, Slide } from 'react-toastify'
import { useDispatch } from 'react-redux'
import { AbilityContext } from '@src/utility/context/Can'
import { handleLogin } from '@store/actions/auth'
import { getHomeRouteForLoggedInUser } from '@utils'
import Avatar from '@components/avatar'
import { Coffee } from 'react-feather'
import "./mfa.css"

const ToastContent = ({ name, role }) => {
  const {t} = useTranslation()
  return (
  <Fragment>
    <div className='toastify-header'>
      <div className='title-wrapper'>
        <Avatar size='sm' color='success' icon={<Coffee size={12} />} />
        <h6 className='toast-title font-weight-bold'>{t("Welcome")}, {name}</h6>
      </div>
    </div>
    <div className='toastify-body'>
      <span>{t("You have successfully logged in as an")} {role} {t("user to XDR. Now you can start to explore. Enjoy!")}</span>
    </div>
  </Fragment>
  )
}

 
const TwoStepsCover = () => {
  const {t} = useTranslation()
  const source = require(`@src/assets/images/pages/loginpagelogo.png`).default
  const [loading, setLoading] = useState(false)
  const { v_token } = useParams()
  const [resendOtp, setResendOtp] = useState(false)
  const [optMsg, setOtpMsg] = useState("")
  
  const ability = useContext(AbilityContext)
  const dispatch = useDispatch()
  const history = useHistory()
  const [OTP, setOTP] = useState("")

  const mfa_login = (event) => {
    event.preventDefault()
    
    if (OTP.length < 6) {
        setOtpMsg(<span className='text-danger'>{t("Enter all 6 digit of OTP")}</span>)
        return false
    }

    setLoading(true)

    axios.post('/mfa-verity-otp', {
      v_token,
      mail_otp: OTP
    }).then(res => {
      setLoading(false)
      
      if (res.data.message_type === "login_success") {
        const data = { ...res.data.bk_data, accessToken: res.data.token.access, refreshToken: res.data.token.refresh }
        dispatch(handleLogin(data))
        ability.update(data.ability)
        history.push(getHomeRouteForLoggedInUser(data.role))
        toast.success(
          <ToastContent name={data.username} role={data.role} />,
          { transition: Slide, hideProgressBar: true, autoClose: 2000 }
        )
        
      }
     
    }).catch(error => {
      setLoading(false)
      if (error.response) {
        if (error.response.data) {
          const res = error.response.data
          setOtpMsg("invalid otp")
          if (res.message_type = "invalid_otp") {
            toast.warn("Invalid OTP", {
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
      }
    })
  }

  const OtpResendHandle = () => {
    if (v_token !== "") {
        setResendOtp(true)
        const fromDataOTP = new FormData()
        fromDataOTP.append("action", "MAF_RESEND")
        fromDataOTP.append("MFA_token", v_token)
        axios({
            url: "/resend-otp",
            method: "post",
            data:fromDataOTP
        }).then((res) => {
            setResendOtp(false)
            if (res.data.message_type === "otp_resend_on_mail") {
                setOtpMsg("Please check your emails for a message with your code. Your code is 6 numbers long.")
            }
        }).catch((error) => {
            setResendOtp(false)
        })
    }
  }

  return (
    <div className='auth-wrapper auth-cover'>
      <Row className='auth-inner m-0'>
        <Link className='brand-logo' to='/' >
          <img src={img2} width="200px" height="50px" />
        </Link>
        <Col className='d-none d-lg-flex align-items-center p-5' lg='8' sm='12'>
          <div className='w-100 d-lg-flex align-items-center justify-content-center px-5'>
            <img className='img-fluid' src={source} alt='Login Cover' />
          </div>
        </Col>
        <Col className='d-flex align-items-center auth-bg px-2 p-lg-5' lg='4' sm='12'>
          <Col className='px-xl-2 mx-auto' sm='8' md='6' lg='12'>
            <CardTitle tag='h2' className='fw-bolder mb-1'>
              {t("Two Step Verification")}💬
            </CardTitle>
            <CardText className='mb-75'>
            {t("We sent a verification code to your registered email address. Enter the code from the email in the field below")}
            </CardText>
            <Form className='mt-2' onSubmit={mfa_login}>
              <h6 className='m-1'>{t("Type your 6 digit security code")}</h6>
                <OTPInput value={OTP} onChange={setOTP} autoFocus OTPLength={6} otpType="number" className="otp-input-main-box"  inputClassName="otp-input-box" />
              <Badge color='warning' className='badge-glow mt-1'>
              {(optMsg !== "") ? optMsg : ""}
             </Badge>             
            
              <div className='mt-1'>
              {(loading === false) ? <Button.Ripple color='primary' block>{t("Sign in")}</Button.Ripple> : <Button.Ripple type="button" color='primary' block disabled> <Spinner size="sm" />{t("Login")}...</Button.Ripple> }
              </div>
            </Form>
            <p className='text-right m-1'>
              <span>{t("Didn’t get the code?")}</span>
              {(!resendOtp) ? <span className='text-primary' style={{ cursor: "pointer" }} onClick={OtpResendHandle}>{t("Resend")}</span> : <Spinner size="sm" className='text-primary' />}
            </p>
          </Col>
        </Col>
      </Row>
    </div>
  )
}

export default TwoStepsCover