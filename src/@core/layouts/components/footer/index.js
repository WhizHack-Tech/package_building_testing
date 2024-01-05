// =============================================================================================
//  File Name: footer\index.js
//  Description: Details of the footer component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** Icons Import
import { Heart } from 'react-feather'
import ReactCountryFlag from 'react-country-flag'
import { FormattedMessage } from 'react-intl'
import { useTranslation } from 'react-i18next'

const Footer = () => {
  const {t} = useTranslation()
  return (
    <p className='clearfix mb-0'>
      <span className='float-md-left d-block d-md-inline-block mt-25'>
      <FormattedMessage id='COPYRIGHT' /> © {new Date().getFullYear()}{' '}
        <a href='https://www.whizhack.com/' target='_blank' rel='noopener noreferrer'>
         WHIZHACK
        </a>
        <span className='d-none d-sm-inline-block'>, {t('All rights Reserved')}</span>
      </span>
      <span className='float-md-right d-none d-md-block'>
        {t('Made in INDIA')}       
        <ReactCountryFlag className='ml-1' countryCode='in' svg  size={14} />
      </span>
    </p>
  )
}

export default Footer
