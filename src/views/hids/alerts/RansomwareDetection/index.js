import { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardBody, Table, CardSubtitle, Button, Modal, ModalHeader, ModalBody, Spinner, Badge } from 'reactstrap'
import axios from "@axios"
import { Link } from 'react-router-dom'
import { useSelector } from "react-redux"
import { useTranslation } from 'react-i18next'
import { token } from '@utils'
import PreLoader from '../../preLoader'
import { Cpu } from 'react-feather'
import Avatar from '@components/avatar'
const Nidstype = () => {
  const { t } = useTranslation()
  const [shortTableData, setTableData] = useState([])
  const [criticalThreatsTotal, setCriticalThreatsTotal] = useState([])
  const [apiLoader, setApiLoader] = useState(false)
  const [modalBox, setModalBox] = useState(false)
  const filterState = useSelector((store) => store.dashboard_chart)
  const [checkApiData, setCheckApiData] = useState(true)

  const apiLogic = () => {

    setApiLoader(true)

    axios.get(`/hids-alert-potential-ransomware?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)

        if (res.data.message_type === "d_not_f") {
          setCheckApiData(false)
        }

        if (res.data.message_type === "success") {
          setCheckApiData(true)
          setCriticalThreatsTotal(res.data.count)
          setTableData(res.data.filter)


        }

      })
      .catch(error => {
        setApiLoader(false)
        console.log(error.message)
      })
  }

  useEffect(() => {
    apiLogic()

  }, [filterState.values, filterState.refreshCount])

  return (
    <Card>
      <CardHeader>
        <CardTitle className='mb-75' tag='h4'>

        </CardTitle>
        <div className='round overflow-hidden round overflow-hidden'>
          <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
            View More
          </Button.Ripple>
        </div>
        <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='xl'>
          <ModalHeader>{t('Ransomware')}</ModalHeader>
          <ModalBody>
            <Table striped responsive>
              <thead>
                <tr>
                  <th>{t('Agent ID')}</th>
                  <th>{t('Name')}</th>
                  <th>{t('Agent IP')}</th>
                  <th>{t('Count')}</th>
                  <th>{t('Actions')}</th>
                </tr>
              </thead>
              <tbody>
                {(shortTableData.length === 0 || checkApiData === false) ? (
                  <tr>
                    <td colSpan={7} className='text-center'>{t('Data Not Found')}</td>
                  </tr>
                ) : (
                  shortTableData.map((rows, index) => {
                    return (
                      <tr key={index}>
                        <td>
                          <span className='align-middle fw-bold'>{rows.agent_id}</span>
                        </td>
                        <td>
                          <span className='align-middle fw-bold'>Ransomware Potential</span>
                        </td>
                        <td>
                          <span className='align-middle fw-bold'>{rows.agent_ip}</span>
                        </td>
                        <td>
                          <span className='align-middle fw-bold'>{rows.ransomware_count}</span>
                        </td>
                        <td>
                          <Link to={`/hids-alert-ransomware-details?current_time=${rows.current_time}&past_time=${rows.past_time}&agent_id=${rows.agent_id}&agent_ip=${rows.agent_ip}&ransomware_count=${rows.ransomware_count}`} className='btn-sm btn-outline-primary m-2'>
                            {t('More Details')}
                          </Link>
                        </td>
                      </tr>
                    )
                  })
                )
                }
              </tbody>
            </Table>
          </ModalBody>
        </Modal>
      </CardHeader>
      <CardBody className='text-center'>
        {checkApiData ? (
          <div>
            <h1 className='font-weight-bolder mt-2'>{criticalThreatsTotal}</h1>
            <p>Ransomware Event</p>
          </div>
        ) : (
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
            <p>{t('Data Not Found')}</p>
          </div>
        )}
      </CardBody>
      {apiLoader ? <PreLoader /> : null}
    </Card>

  )
}

export default Nidstype 