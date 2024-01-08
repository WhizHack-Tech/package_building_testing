// ================================================================================================
//  File Name: Login.js
//  Description: Details of the Login Page.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import { useState, useContext, Fragment } from 'react'
import Avatar from '@components/avatar'
import { useDispatch } from 'react-redux'
import { toast, Slide } from 'react-toastify'
import { handleLogin } from '@store/actions/auth'
import { AbilityContext } from '@src/utility/context/Can'
import { Link, useHistory } from 'react-router-dom'
import InputPasswordToggle from '@components/input-password-toggle'
import { getHomeRouteForLoggedInUser } from '@utils'
import { Coffee } from 'react-feather'
import { AvForm, AvInput } from 'availity-reactstrap-validation-safe'
import {
  Alert,
  Row,
  Col,
  CardTitle,
  Spinner,
  FormGroup,
  Label,
  Button
} from 'reactstrap'

import axios from '../axios'
import img2 from '@src/assets/images/logo/Logo2.png'

import '@styles/base/pages/page-auth.scss'

const ToastContent = ({ name, role }) => (
  <Fragment>
    <div className='toastify-header'>
      <div className='title-wrapper'>
        <Avatar size='sm' color='success' icon={<Coffee size={12} />} />
        <h6 className='toast-title font-weight-bold'>Welcome, {name}</h6>
      </div>
    </div>
    <div className='toastify-body'>
      <span>You have successfully logged in as an {role} user to XDR Master. Now you can start to explore. Enjoy!</span>
    </div>
  </Fragment>
)

const Login = () => {
  const ability = useContext(AbilityContext)
  const dispatch = useDispatch()
  const history = useHistory()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const source = require(`@src/assets/images/pages/loginpagelogo.png`).default

  const handleSubmit = (event, errors) => {
    setLoading(true)
    if (errors && !errors.length) {
      axios.post('/master-login', {
        email,
        password
      })
        .then((res) => {
          setLoading(false)
          if (res.data) {
            if (res.data.message_type === "login_success") {
              const data = { ...res.data.bk_data, accessToken: res.data.token.access, refreshToken: res.data.token.refresh }
              dispatch(handleLogin(data))
              ability.update(data.ability)
              history.push(getHomeRouteForLoggedInUser(data.role))
              toast.success(
                <ToastContent name={data.name} role={data.role} />,
                { transition: Slide, hideProgressBar: true, autoClose: 2000 }
              )

            }
          }
        })
        .catch((error) => {
          setLoading(false)
          if (error.response) {
            if (error.response.data) {
              const res = error.response.data
              if (res.message_type === "user_not_exist") {
                toast.warn('User ID or Password is Wrong', {
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
          <h2 className='display-4 ml-0'>XDR MASTER</h2> <br />
        </Link>
        <Col className='d-none d-lg-flex align-items-center p-5' lg='8' sm='12'>
          <div className='w-100 d-lg-flex align-items-center justify-content-center px-5'>
            <img className='img-fluid' src={source} alt='Login V2' />
          </div>
        </Col>
        <Col className='d-flex align-items-center auth-bg px-2 p-lg-5' lg='4' sm='12'>
          <Col className='px-xl-2 mx-auto' sm='8' md='6' lg='12'>
            <CardTitle tag='h2' className='font-weight-bold mb-1'>
              Welcome to XDR Master
            </CardTitle>
            <Alert color='primary'>
            </Alert>
            <AvForm className='auth-login-form mt-2' onSubmit={handleSubmit}>
              <FormGroup>
                <Label className='form-label' for='login-email'>
                  Email
                </Label>
                <AvInput
                  required
                  autoFocus
                  type='email'
                  value={email}
                  id='login-email'
                  name='login-email'
                  placeholder='john@example.com'
                  onChange={e => setEmail(e.target.value)}
                />
              </FormGroup>
              <FormGroup>
                <div className='d-flex justify-content-between'>
                  <Label className='form-label' for='login-password'>
                    Password
                  </Label>
                </div>
                <InputPasswordToggle
                  required
                  tag={AvInput}
                  value={password}
                  id='login-password'
                  name='login-password'
                  className='input-group-merge'
                  onChange={e => setPassword(e.target.value)}
                />
              </FormGroup>
              {(loading === false) ? <Button.Ripple color='primary' block disabled={!email.length || !password.length}> Sign in </Button.Ripple> : <Button.Ripple type="button" color='primary' block disabled> <Spinner size="sm" /> Login... </Button.Ripple>}

            </AvForm>
          </Col>
        </Col>
      </Row>
    </div>
  )
}

export default Login
