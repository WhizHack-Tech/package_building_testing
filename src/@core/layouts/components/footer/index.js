// ==============================================================================================
//  File Name: footer/index.js
//  Description: Details of the footer component.
//  ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** Icons Import
import { Heart } from 'react-feather'
import ReactCountryFlag from 'react-country-flag'

const Footer = () => {
  return (
    <p className='clearfix mb-0'>
      <span className='float-md-left d-block d-md-inline-block mt-25'>
        COPYRIGHT © {new Date().getFullYear()}{' '}
        <a href='https://www.whizhack.com/' target='_blank' rel='noopener noreferrer'>
          WHIZHACK
        </a>
        <span className='d-none d-sm-inline-block'>, All rights Reserved</span>
      </span>
      <span className='float-md-right d-none d-md-block'>
        Made in INDIA
        <ReactCountryFlag className='ml-1' countryCode='in' svg  size={14} />
      </span>
    </p>
  )
}

export default Footer
