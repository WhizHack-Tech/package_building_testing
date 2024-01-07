// ================================================================================================
//  File Name: Notification.js
//  Description: Details of the Notification.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useState, useEffect } from 'react'
import Timeline from '@components/timeline/notificationUI'
import { Card, CardBody } from 'reactstrap'
import { Shield } from 'react-feather'
import '@styles/react/apps/app-email.scss'
import { useSelector } from "react-redux"
import { useTranslation } from 'react-i18next'

let RenderData = []
const BasicTimeline = () => {
  const { t } = useTranslation()

  const notificationStore = useSelector(store => store.ws_reducer)
  const [oldNotification, setOldNotification] = useState([])

  useEffect(() => {
    try {
      const notificationJson = localStorage.getItem('notification_data')
      setOldNotification(JSON.parse(notificationJson ? notificationJson : []))
    } catch (error) {
      console.log(error.message)
    }
  }, [])

  if (notificationStore.notificationData.notificationRes.length > 0) {
    RenderData = notificationStore.notificationData.notificationRes.map((item) => {
      return {
        icon: <Shield size={14} />,
        color: 'warning',
        objKey: Object.keys(item),
        objVal: Object.values(item)
      }
    })
  } else {
    RenderData = oldNotification.map((item) => {
      return {
        icon: <Shield size={14} />,
        color: 'warning',
        objKey: Object.keys(item),
        objVal: Object.values(item)
      }
    })
  }

  return (
    <Card>
      <CardBody>
        <div className='scroll-box'>
          <Timeline data={RenderData} />
        </div>
        {
          ((notificationStore.notificationData.notificationRes.length <= 0) && (oldNotification.length <= 0)) ? (<div className='text-center mb-2'>{t("Data Not Found")}</div>) : null
        }
      </CardBody>
    </Card>
  )
}

export default BasicTimeline
