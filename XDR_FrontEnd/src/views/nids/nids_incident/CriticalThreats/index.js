// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Incidents ( Critical Threat )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==========================================================================================
import { useEffect, useState } from 'react'
import axios from '@axios'
import Chart from 'react-apexcharts'
import { Link } from 'react-router-dom'
import { useSelector } from 'react-redux'
import PreLoader from '../preLoader'
import { token } from '@utils'
import { Card, CardHeader, CardText, CardBody, Table, CardSubtitle, Button, Modal, ModalHeader, ModalBody, Spinner } from 'reactstrap'
import { useTranslation } from 'react-i18next'
const CriticalThreats = ({ success }) => {
  const [shortTableData, setTableData] = useState([])
  const [criticalThreats, setCriticalThreatsTotal] = useState([])
  const [apiLoader, setApiLoader] = useState(false)
  const [modalBox, setModalBox] = useState(false)
  const filterState = useSelector((store) => store.incident_charts)
  const [checkApiData, setCheckApiData] = useState(true)
  const {t} = useTranslation()
  const apiLogic = () => {
    setApiLoader(true)

    axios.get(`/nids-incident-critical-threats?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)

        if (res.data.message_type === "d_not_f") {
          setCheckApiData(false)
        }

        if (res.data.message_type === "success") {
          setCheckApiData(true)
          setCriticalThreatsTotal(res.data)
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

  const options = {
    chart: {

      toolbar: {
        show: false
      },
      sparkline: {
        enabled: true
      }
    },
    grid: {
      show: true
    },
    colors: ['#90EE90', '#FF0000', '#00FFFF'],
    dataLabels: {
      enabled: false
    },
    stroke: {
      curve: 'smooth',
      width: 2.5
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 0.9,
        opacityFrom: 0.7,
        opacityTo: 0.5,
        stops: [0, 80, 100]
      }
    },

    xaxis: {
      labels: {
        show: false
      },
      axisBorder: {
        show: false
      }
    },
    yaxis: {
      labels: {
        show: false
      }
    },
    tooltip: {
      x: { show: false }
    }
  }

  const series = [
    {
      name: 'Internal',
      data: criticalThreats.internal_compromised_machine || []
    },
    {
      name: 'Lateral',
      data: criticalThreats.lateral_movement || []
    },
    {
      name: 'External Attack',
      data: criticalThreats.external_attack || []
    }
  ]

  return (
    <Card>
      <CardHeader className='align-items-start pb-0'>
        <div>

          {checkApiData ? <h2 className='font-weight-bolder'>{criticalThreats.total}</h2> : null}

          <CardText>{t('Critical Threats')}</CardText>
        </div>
        <div className='round overflow-hidden round overflow-hidden'>
          <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
            {t('View More')}
          </Button.Ripple>
        </div>
        <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
          <ModalHeader>{t('Critical Threats')}</ModalHeader>
          <ModalBody>
            <Table striped responsive>
              <thead>
                <tr>
                  <th>{t('Critical Threats')}</th>
                  <th>{t('Platform')}</th>
                  <th>{t('Counts')}</th>
                  <th>{t('Action')}</th>
                </tr>
              </thead>
              <tbody>
                {
                  (shortTableData.length === 0 || checkApiData === false) ? (
                    <tr>
                      <td colSpan={3} className='text-center'>Data Not Found</td>
                    </tr>
                  ) : (
                    shortTableData.map((rows, index) => (
                      <tr key={index}>
                        <td>
                          <span className='align-middle fw-bold'>{rows.type_of_threat}</span>
                        </td>
                        <td>
                          <span className='align-middle fw-bold'>{rows.platform}</span>
                        </td>
                        <td>
                          <span className='align-middle fw-bold'>{rows.threat_count}</span>
                        </td>
                        <td>
                          <Link to={`/nids-incident-critical-threats-details?current_time=${rows.current_time}&past_time=${rows.past_time}&type_of_threat=${rows.type_of_threat}&platform=${rows.platform}`} className='btn-sm btn-outline-primary m-2'>
                            {t('More Details')}
                          </Link>
                        </td>
                      </tr>
                    ))
                  )
                }
              </tbody>
            </Table>
          </ModalBody>
        </Modal>
      </CardHeader>
      <CardBody>
        {checkApiData ? (
          <Chart options={options} series={series} type='area' height={75} />
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

export default CriticalThreats
