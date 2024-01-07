// ================================================================================================
//  File Name: Error.js
//  Description: Details of the Error ( Error Page ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Button } from 'reactstrap'
import { Link } from 'react-router-dom'
import errorImg from '@src/assets/images/pages/error.svg'
import img2 from '@src/assets/images/logo/Logo4.png'
import '@styles/base/pages/page-misc.scss'
import { useTranslation } from 'react-i18next'

const Error = () => {
  const {t} = useTranslation()
  return (
    <div className='misc-wrapper'>
       <a className='brand-logo' href='/'>
      <img src={img2} width="200px" height="50px" />
      </a>
      <div className='misc-inner p-2 p-sm-3'>
        <div className='w-100 text-center'>
          <h2 className='mb-1'>{t("Page Not Found")}🕵🏻‍♀️</h2>
          <p className='mb-2'>{t("Oops! 😖 The requested URL was not found on this server")}</p>
          <Button tag={Link} to='/' color='primary' className='btn-sm-block mb-2'>
          {t("Back to home")}
          </Button>
          <img className='img-fluid' src={errorImg} alt='Not authorized page' />
        </div>
      </div>
    </div>
  )
}
export default Error
