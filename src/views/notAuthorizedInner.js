// ================================================================================================
//  File Name: notAuthorizedInner.js
//  Description: Details of the Not Authorized Ineer Page.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useTranslation } from 'react-i18next'
import notAuthImg from '@src/assets/images/pages/not-authorized.svg'
import '@styles/base/pages/page-misc.scss'

const NotAuthorizedInner = () => {
  const { t } = useTranslation()

  return (
    <div className='misc-inner p-2 p-sm-3'>
      <div className='w-100 text-center'>
        <h2 className='mb-1'>{t('You are not authorized!')} 🔐</h2>
        <p className='mb-2'>
          {t('You are not authorized! This page is not authorized for you as per your role')}
        </p>
        <img className='img-fluid' src={notAuthImg} alt='Not authorized page' />
      </div>
    </div>
  )
}

export default NotAuthorizedInner
