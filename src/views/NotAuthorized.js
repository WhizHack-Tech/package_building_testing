// ================================================================================================
//  File Name: NotAuthorized.js
//  Description: Details of the NotAuthorized.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import { Button } from 'reactstrap'
import { Link } from 'react-router-dom'
import notAuthImg from '@src/assets/images/pages/not-authorized.svg'
import img2 from '@src/assets/images/logo/Logo2.png'
import '@styles/base/pages/page-misc.scss'

const NotAuthorized = () => {
  return (
    <div className='misc-wrapper'>
      <a className='brand-logo' href='/'>
        <img src={img2} width="250px" height="61px" />
        <h2 className='display-4 ml-0'>XDR MASTER</h2> <br />
      </a>
      <div className='misc-inner p-2 p-sm-3'>
        <div className='w-100 text-center'>
          <h2 className='mb-1'>You are not authorized! 🔐</h2>
          <p className='mb-2'>
            The Webtrends Marketing Lab website in IIS uses the default IUSR account credentials to access the web pages
            it serves.
          </p>
          <Button tag={Link} to='/' color='primary' className='btn-sm-block mb-1'>
            Back to login
          </Button>
          <img className='img-fluid' src={notAuthImg} alt='Not authorized page' />
        </div>
      </div>
    </div>
  )
}
export default NotAuthorized
