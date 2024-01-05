// =============================================================================================
//  File Name: navbar/index.js
//  Description: Details of the ToastContent component.
// ---------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

// ** React Imports
import { Fragment, useEffect } from 'react'
import { toast, Slide } from 'react-toastify'
import { useSelector } from "react-redux"
import { Shield } from 'react-feather'
import NavbarUser from './NavbarUser'
import { useHistory } from "react-router-dom"
import Avatar from '@components/avatar'
import { t } from 'i18next'

const ToastContent = ({ msg, moreNotification }) => {

  return <div onClick={() => { moreNotification() }}>
    <div className='toastify-header'>
      <div className='title-wrapper'>
        <Avatar size='sm' color='warning' icon={<Shield size={12} />} />
        <h6 className='text-warning ml-50 mb-0'>{t('Security Warning')}</h6>
      </div>
    </div>
    <div className='toastify-body'>
      <span className='text-dark'><span className='text-warning font-weight-bold'>{msg}</span>{t(' Numbers of security warning in your environment, click on the')}<span className="text-primary font-weight-bold" onClick={() => { moreNotification() }}>{t(' View More')}</span>{t(' to get the details')}</span>
    </div>
  </div>
}

const ThemeNavbar = props => {
  // ** Props
  const { skin, setSkin, setMenuVisibility } = props
  const notificationStore = useSelector(store => store.ws_reducer)
  const history = useHistory()

  const moreNotification = () => {
    history.push("/settings/notification")
  }

  useEffect(() => {
    if (notificationStore.notificationData.notificationRes.length > 0) {
      toast.success(
        <ToastContent moreNotification={moreNotification} msg={notificationStore.notificationData.notificationRes.length} />,
        { transition: Slide, hideProgressBar: true, autoClose: 5000 }
      )
    }
  }, [notificationStore.notificationData.notificationRes.length])

  return (
    <Fragment>
      {/* <div className='bookmark-wrapper d-flex align-items-center'>
        <NavbarBookmarks setMenuVisibility={setMenuVisibility} />
      </div> */}
      <NavbarUser skin={skin} setSkin={setSkin} />
    </Fragment>
  )
}

export default ThemeNavbar
