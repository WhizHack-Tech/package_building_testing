// ================================================================================================
//  File Name: Logs.js
//  Description: User Config Details.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ================================================================================================

// ** React imports   
import Timeline from '@components/timeline'
import { useState, useEffect } from 'react'
import axios from '@axios'
import { Activity } from 'react-feather'
import { Card, CardBody, CardHeader, CardTitle, Spinner, Alert } from 'reactstrap'
import { useParams } from "react-router-dom"
// ** Utils
import { token } from '@utils'
import '@styles/react/apps/app-email.scss'
import { format } from 'date-fns'

const IconsTimeline = () => {
  // ** State 
  const [userLogs, setUserLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const { id } = useParams()
  // 
  useEffect(() => {
    axios.get(`/user-api-logs?uid=${id}`, { headers: { Authorization: token() } }).then(res => {
      setUserLogs(res.data.data)
      setLoading(true)
    }).finally(() => {
      setLoading(false)
    })
  }, [])
  const dataRenderLogs = userLogs.map((data, key) => {
    return {
      title: `Activity : ${data.description}`,
      icon: <Activity size={14} />,
      content: `Browser : ${data.browser_type}`,
      customContent: `IP : ${data.ip}`,
      method: `Method : ${data.req_method}`,
      type: `Type : ${data.type}`,
      meta: <Alert color='primary' className='text-uppercase'>{format(new Date(data.date_time), "yyyy-MM-dd, h:mm:ss a")}</Alert>,
      username: `Username : ${(data.first_name !== undefined) ? data.first_name : ""} ${(data.last_name !== undefined) ? data.last_name : ""}`,
      color: "primary",
      key
    }
  })

  return (
    <Card>
      {loading ? <div className='d-flex justify-content-center'><Spinner color='primary' type='grow' /></div> : ""}
      <CardBody>
        <div className='scroll-box'>
          <Timeline data={dataRenderLogs} />
        </div>
      </CardBody>
    </Card>
  )
}

export default IconsTimeline