// =============================================================================================
//  File Name: IntlDropdown.js
//  Description: Details of the IntlDropdown component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** React Imports
import { useContext, useEffect } from 'react'
import { useTranslation } from 'react-i18next'

// ** Third Party Components
import ReactCountryFlag from 'react-country-flag'
import { UncontrolledDropdown, DropdownMenu, DropdownItem, DropdownToggle } from 'reactstrap'

// ** Internationalization Context
import { setLang, getLang, token } from '@utils'
import axios from '@axios'
import {useSelector, useDispatch} from "react-redux"
import { handleRTL } from '@store/actions/layout'
const IntlDropdown = () => {
  
  const { i18n } = useTranslation()
  
  const dispatch = useDispatch()
  
  const langTypeCheck = useSelector((store) => store.langSwitch.langType)

  // ** Vars
  const langObj = {
    en: 'English',
    de: 'German',
    fr: 'French',
    pt: 'Portuguese',
    jp: 'Japanese',
    in: 'Hindi',
    sa: 'Arabic'
  }

  // ** Function to switch Language
  const handleLangUpdate = (e, lang) => {
    e.preventDefault()
    i18n.changeLanguage(lang)
    
    if (lang !== undefined && lang === 'sa') {
      dispatch(handleRTL(true))
    } else {
      dispatch(handleRTL(false))
    }

    setLang(lang)
    axios.post(`/dashboard-lang-update`, 
    {lang_type:lang},
    { headers: { Authorization: token() } }
    ).then(res => {
      if (res.data.message_type === "form_errors" || res.data.message_type === "user_id_not_found") {
        console.log("something is wrong.")
      }
    })
    
  }

  useEffect(() => {
    if (langTypeCheck !== undefined && langTypeCheck === 'sa') {
      dispatch(handleRTL(true))
    } else {
      dispatch(handleRTL(false))
    }
  }, [])

  useEffect(() => {
    setLang(langTypeCheck)
    i18n.changeLanguage(langTypeCheck)
}, [langTypeCheck])

  return (
   <UncontrolledDropdown href='/' tag='li' className='dropdown-language nav-item'>
      <DropdownToggle href='/' tag='a' className='nav-link' onClick={e => e.preventDefault()}>
        <ReactCountryFlag
          className='country-flag flag-icon'
          countryCode={i18n.language === 'en' ? 'us' : i18n.language}
          svg
        />
        <span className='selected-language'>{langObj[i18n.language]}</span>
      </DropdownToggle>
      <DropdownMenu className='mt-0' right>
        <DropdownItem href='/' tag='a' onClick={e => handleLangUpdate(e, 'en')}>
          <ReactCountryFlag className='country-flag' countryCode='us' svg />
          <span className='ml-1'>English</span>
        </DropdownItem>
        <DropdownItem href='/' tag='a' onClick={e => handleLangUpdate(e, 'fr')}>
          <ReactCountryFlag className='country-flag' countryCode='fr' svg />
          <span className='ml-1'>French</span>
        </DropdownItem>
        <DropdownItem href='/' tag='a' onClick={e => handleLangUpdate(e, 'de')}>
          <ReactCountryFlag className='country-flag' countryCode='de' svg />
          <span className='ml-1'>German</span>
        </DropdownItem>
        <DropdownItem href='/' tag='a' onClick={e => handleLangUpdate(e, 'jp')}>
          <ReactCountryFlag className='country-flag' countryCode='jp' svg />
          <span className='ml-1'>Japanese</span>
        </DropdownItem>
        <DropdownItem href='/' tag='a' onClick={e => handleLangUpdate(e, 'in')}>
          <ReactCountryFlag className='country-flag' countryCode='in' svg />
          <span className='ml-1'>Hindi</span>
        </DropdownItem>
        <DropdownItem href='/' tag='a' onClick={e => handleLangUpdate(e, 'sa')}>
          <ReactCountryFlag className='country-flag' countryCode='sa' svg />
          <span className='ml-1'>Arabic</span>
        </DropdownItem>
      </DropdownMenu>
    </UncontrolledDropdown>
  )
}

export default IntlDropdown
