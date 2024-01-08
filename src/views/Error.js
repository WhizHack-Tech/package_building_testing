// ================================================================================================
//  File Name: Error.js
//  Description: Details of the Error Page.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import { Button } from 'reactstrap'
import { Link } from 'react-router-dom'
import errorImg from '@src/assets/images/pages/error.svg'
// import img2 from '@src/assets/images/logo/Logo2.png'
import img2 from '@src/assets/images/logo/Logo2.png'
import '@styles/base/pages/page-misc.scss'

const Error = () => {
  return (
    <div className='misc-wrapper'>
      <a className='brand-logo' href='/'>
        <img src={img2} width="250px" height="61px" />
        <h2 className='display-4 ml-0'>XDR MASTER</h2> <br />
      </a>
      <div className='misc-inner p-2 p-sm-3'>
        <div className='w-100 text-center'>
          <h2 className='mb-1'>Page Not Found 🕵🏻‍♀️</h2>
          <p className='mb-2'>Oops! 😖 The requested URL was not found on this server.</p>
          <Button tag={Link} to='/' color='primary' className='btn-sm-block mb-2'>
            Back to home
          </Button>
          <img className='img-fluid' src={errorImg} alt='Not authorized page' />
        </div>
      </div>
    </div>
  )
}
export default Error
