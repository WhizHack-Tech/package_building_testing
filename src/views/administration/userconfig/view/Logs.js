// ================================================================================================
//  File Name: Logs.js
//  Description: Details of the Administration ( View User Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import Timeline from '@components/timeline'
import { useState, useEffect } from 'react'
import axios from '@axios'
import { Activity } from 'react-feather'
import { Card, CardBody, CardHeader, Alert, Spinner } from 'reactstrap'
import { useParams } from 'react-router-dom'
import { format } from 'date-fns'
import "../Loader.css"
// ** Utils
import { token } from '@utils'
import '@styles/react/apps/app-email.scss'

const IconsTimeline = () => {
  const [userLogs, setUserLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const { id } = useParams()

  useEffect(() => {
    axios
      .get(`/user-api-logs?uid=${id}`, { headers: { Authorization: token() } })
      .then((res) => {
        setUserLogs(res.data.data)
        setLoading(false)
      })
      .catch((error) => {
        console.log(error)
        setLoading(false)
      })
  }, [])

  const dataRenderLogs = userLogs.map((data, key) => {
    return {
      title: `Activity: ${data.description}`,
      icon: <Activity size={14} />,
      content: `Browser: ${data.browser_type}`,
      customContent: `IP: ${data.ip}`,
      method: `Method: ${data.req_method}`,
      type: `Type: ${data.type}`,
      meta: (
        <Alert color='primary' className='text-uppercase'>
          {format(new Date(data.date_time), 'yyyy-MM-dd, h:mm:ss a')}
        </Alert>
      ),
      email: `Email ID: ${data.email_id}`,
      // username: `Username: ${(data.first_name !== undefined) ? data.first_name : ""} ${(data.last_name !== undefined) ? data.last_name : ""}`,
      color: 'primary',
      key
    }
  })

  return (
    <Card>
      <CardBody>
        {loading ? (
          <div className='d-flex justify-content-center align-items-center' style={{ height: '210px' }}>
           <div class="tri-color-ripple-spinner">
           <div class="ripple ripple1"></div>
           <div class="ripple ripple2"></div>
         </div>
         </div>
        ) : userLogs.length === 0 ? (
          <div className='text-center'>Data not found</div>
        ) : (
          <div className='scroll-box'>
            <Timeline data={dataRenderLogs} />
          </div>
        )}
      </CardBody>
    </Card>
  )
}

export default IconsTimeline
