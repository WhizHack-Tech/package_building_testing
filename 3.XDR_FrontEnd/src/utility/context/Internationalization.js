// =============================================================================================
//  File Name: Internationalization.js
//  Description: Details of the Internationalization Utility component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** React Imports
import { useState, createContext, useEffect, useContext } from 'react'

// ** Intl Provider Import
import { IntlProvider } from 'react-intl'

// ** Core Language Data
import messagesEn from '@assets/data/locales/en.json'
import messagesDe from '@assets/data/locales/de.json'
import messagesFr from '@assets/data/locales/fr.json'
import messagesPt from '@assets/data/locales/pt.json'
import messagesJp from '@assets/data/locales/jp.json'
import messagesIn from '@assets/data/locales/hindi.json'
import messagesSa from '@assets/data/locales/sa.json'

import { setLang, getLang, token, isUserLoggedIn } from '@utils'
import axios from '@axios'
import {useSelector, useDispatch} from "react-redux"
import { langSwitch } from '../../redux/actions/layout/lang_switch'

// ** Menu msg obj
const menuMessages = {
  en: { ...messagesEn },
  de: { ...messagesDe },
  fr: { ...messagesFr },
  pt: { ...messagesPt },
  jp: { ...messagesJp },
  in: { ...messagesIn },
  sa: { ...messagesSa }
}

// ** Create Context
const Context = createContext()

const IntlProviderWrapper = ({ children }) => {
  // ** States
  const dispatch = useDispatch()
  const [locale, setLocale] = useState(getLang)
  const [messages, setMessages] = useState(menuMessages[getLang])
  const langTypeCheck = useSelector((store) => store.langSwitch.langType)
  // ** Switches Language
  const switchLanguage = lang => {
    setLocale(lang)
    setMessages(menuMessages[lang])
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
    if (isUserLoggedIn() !== null) {
      dispatch(langSwitch())
    }
  }, [])

  useEffect(() => {
      setLocale(langTypeCheck)
      setMessages(menuMessages[langTypeCheck])
      setLang(langTypeCheck)
  }, [langTypeCheck])

  return (
    <Context.Provider value={{ locale, switchLanguage }}>
      <IntlProvider key={locale} locale={locale} messages={messages} defaultLocale='en'>
        {children}
      </IntlProvider>
    </Context.Provider>
  )
}

export { IntlProviderWrapper, Context as IntlContext }
