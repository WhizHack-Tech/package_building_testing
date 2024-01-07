// ================================================================================================
//  File Name: Login.js
//  Description: Details of the Login.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { useState, useContext, Fragment } from 'react'
import Avatar from '@components/avatar'
import { useDispatch } from 'react-redux'
import { toast, Slide } from 'react-toastify'
import { handleLogin } from '@store/actions/auth'
import { AbilityContext } from '@src/utility/context/Can'
import { Link, useHistory } from 'react-router-dom'
import InputPasswordToggle from '@components/input-password-toggle'
import { getHomeRouteForLoggedInUser } from '@utils'
import { encryptPlayload } from '@src/utility/cryptoHelper'
import { Coffee } from 'react-feather'
import { AvForm, AvInput } from 'availity-reactstrap-validation-safe'
import axios from "@axios"
import { useTranslation } from 'react-i18next'
import img2 from '@src/assets/images/logo/Logo4.png'

import {
  Alert,
  Row,
  Col,
  CardTitle,
  FormGroup,
  Label,
  Button,
  Spinner,
  UncontrolledDropdown
} from 'reactstrap'
import Animate from "./Animate"
import { langSwitch } from '../redux/actions/layout/lang_switch'
import '@styles/base/pages/page-auth.scss'

const ToastContent = ({ name, role }) => {
  const { t } = useTranslation()
  return (
    <Fragment>
      <div className='toastify-header'>
        <div className='title-wrapper'>
          <Avatar size='sm' color='success' icon={<Coffee size={12} />} />
          <h6 className='toast-title font-weight-bold'>{t('Welcome')}, {name}</h6>
        </div>
      </div>
      <div className='toastify-body'>
        <span>{t('You have successfully logged in as an')} {role} {t('user to XDR. Now you can start to explore. Enjoy!')}</span>
      </div>
    </Fragment>
  )
}

const Login = props => {
  const { t } = useTranslation()
  const ability = useContext(AbilityContext)
  const dispatch = useDispatch()
  const history = useHistory()
  const [loading, setLoading] = useState(false)

  const handleSubmit = (event, errors) => {
    if (errors && !errors.length) {
      const payload = encryptPlayload({
        email: event.target.email_id.value,
        password: event.target.login_pass.value
      })

      setLoading(true)

      axios.post('/client-login', {
        payload
      })
        .then((res) => {
          setLoading(false)
          if (res.data) {
            if (res.data.message_type === "login_success") {
              const data = { ...res.data.bk_data, accessToken: res.data.token.access, refreshToken: res.data.token.refresh, default_page: res.data.default_page }
              dispatch(handleLogin(data))
              dispatch(langSwitch())
              ability.update(data.ability)
              history.push(getHomeRouteForLoggedInUser(data.role, data.default_page))
              toast.success(
                <ToastContent name={data.username} role={data.role} />,
                { transition: Slide, hideProgressBar: true, autoClose: 2000 }
              )
            }

            if (res.data.message_type === "verify_mfa") {
              history.push(`/mfa-login/${res.data.v_token}`)
            }
          }
        })
        .catch((error) => {
          setLoading(false)
          if (error.response) {
            if (error.response.data) {
              const res = error.response.data
              if (res.message_type === "form_errors") {
                if (res.errors.non_field_errors !== undefined) {
                  if (res.errors.non_field_errors[0] === "email_not_verify") {
                    toast.warn('Your email has not been verified yet, please check your email', {
                      position: "top-right",
                      autoClose: 5000,
                      hideProgressBar: false,
                      closeOnClick: true,
                      pauseOnHover: true,
                      draggable: true,
                      progress: undefined
                    })
                  }
                  if (res.errors.non_field_errors[0] === "organization_is_disabled") {
                    toast.warn('Your organization is deactived from XDR Portal', {
                      position: "top-right",
                      autoClose: 5000,
                      hideProgressBar: false,
                      closeOnClick: true,
                      pauseOnHover: true,
                      draggable: true,
                      progress: undefined
                    })
                  }

                  if (res.errors.non_field_errors[0] === "account_deactive") {
                    toast.warn('Your account has been deactivated from the admin', {
                      position: "top-right",
                      autoClose: 5000,
                      hideProgressBar: false,
                      closeOnClick: true,
                      pauseOnHover: true,
                      draggable: true,
                      progress: undefined
                    })
                  }
                } else {
                  toast.error("Something is wrong.", {
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

              if (res.message_type === "user_not_exist") {
                toast.warn(res.message, {
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
          } else {
            console.warn('API Error : ', error.message)
          }
        })
    }
  }

  return (
    <div className='auth-wrapper auth-v2'>

      <Row className='auth-inner m-0'>

        <Link className='brand-logo' to='/' onClick={e => e.preventDefault()}>
          <img src={img2} width="250px" height="61px" />
        </Link>
        <Col className='d-none d-lg-flex align-items-center p-5' lg='8' sm='12'>
          <div className='w-100 d-lg-flex align-items-center justify-content-center px-1' >
            <Animate />
          </div>
        </Col>

        <Col className='d-flex align-items-center auth-bg px-2 p-lg-5' lg='4' sm='12'>

          <Col className='px-xl-2 mx-auto' sm='8' md='6' lg='12'>
            <h3 className='d-flex align-items-center auth-bg px-0 p-lg-51'>Security Remediation Console (SRC)</h3>  <br />
            <UncontrolledDropdown className='dropdown-language nav-item'>
            </UncontrolledDropdown>
            <CardTitle tag='h3' className='font-weight-bold mb-1'>
              {t('Login Details')}
            </CardTitle>
            <Alert color='primary'>

            </Alert>
            <AvForm className='auth-login-form mt-2' onSubmit={handleSubmit}>
              <FormGroup>
                <Label className='form-label' for='email'>
                  {t('Email')}
                </Label>
                <AvInput
                  required
                  autoFocus
                  type='email'
                  id='email'
                  name='email_id'
                />
              </FormGroup>
              <FormGroup>
                <div className='d-flex justify-content-between'>
                  <Label className='form-label' for='login-password'>
                    {t('Password')}
                  </Label>
                </div>
                <InputPasswordToggle
                  required
                  tag={AvInput}
                  id='login-password'
                  name='login_pass'
                  className='input-group-merge'
                  autoComplete='off'
                />
              </FormGroup>
              {(loading === false) ? <Button.Ripple color='primary' block>{t('Sign in')}</Button.Ripple> : <Button.Ripple type="button" color='primary' block disabled> <Spinner size="sm" />&nbsp;{t('Login')}...</Button.Ripple>}
            </AvForm>
            <p className='mt-2 text-primary' onClick={() => { history.push("/forgot-password") }} style={{ cursor: "pointer" }}>{t('Forgot Password?')}</p>
          </Col>
        </Col>
      </Row>
    </div>
  )
}

export default Login