// ================================================================================================
//  File Name: NotAuthorized.js
//  Description: Details of the Not Authorized Page.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Button } from 'reactstrap'
import { Link, useHistory } from 'react-router-dom'
import notAuthImg from '@src/assets/images/pages/not-authorized.svg'
import img2 from '@src/assets/images/logo/Logo4.png'
import '@styles/base/pages/page-misc.scss'

const NotAuthorized = () => {
  const history = useHistory()
  const backButton = () => {
    localStorage.removeItem('clientData')
    history.push("/login")
  }
  return (
    <div className='misc-wrapper'>
      <a className='brand-logo' href='/'>
      <img src={img2} width="200px" height="50px" />
      </a>
      <div className='misc-inner p-2 p-sm-3'>
        <div className='w-100 text-center'>
          <h2 className='mb-1'>You are not authorized! 🔐</h2>
          <p className='mb-2'>
            You are not authorized! This page is not authorized for you as per your role.
          </p>
          <Button onClick={backButton}  color='primary' className='btn-sm-block mb-1'>
            Back to login
          </Button>
          <img className='img-fluid' src={notAuthImg} alt='Not authorized page' />
        </div>
      </div>
    </div>
  )
}
export default NotAuthorized
