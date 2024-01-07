// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Events ( Internal Attacks Counts )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { useEffect, useState } from 'react'
import axios from '@axios'
import Chart from 'react-apexcharts'
import { Link } from 'react-router-dom'
import { useSelector } from 'react-redux'
import PreLoader from '../preLoader'
import DataNotFound from '../dNotf'
import { token } from '@utils'
import '@styles/react/libs/tables/react-dataTable-component.scss'
import { Card, CardHeader, CardText, CardBody, Table, Button, Modal, ModalHeader, ModalBody } from 'reactstrap'
import { useTranslation } from 'react-i18next'
const ActiveUsers = ({ success }) => {
  const {t} = useTranslation()
  const [shortTableData, setTableData] = useState([])
  const [criticalThreatsTotal, setCriticalThreatsTotal] = useState(0)

  const [apiLoader, setApiLoader] = useState(false)
  const [modalBox, setModalBox] = useState(false)
  const filterState = useSelector((store) => store.dashboard_chart)
  const [checkApiData, setCheckApiData] = useState(true)

  const apiLogic = () => {

    setApiLoader(true)

    axios.get(`/nids-alert-int-compr?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
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
    colors: ['#90EE90'],
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
        show: true
      }
    },
    yaxis: {
      labels: {
        show: false
      }
    },
    tooltip: {
      x: { show: true }
    }
  }
  const series = [
    {
      data: criticalThreatsTotal.internal_compromised_machine || [],
      name: 'Internal Count'
    }
  ]
  return (
    <Card>
      <CardHeader className='align-items-start pb-0'>
        <div>
          <h2 className='font-weight-bolder'>{checkApiData ? criticalThreatsTotal.total : null}</h2>
          <CardText>{t('Internal Attacks')}</CardText>
        </div>
        <div className='round overflow-hidden round overflow-hidden'>
          <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
            {t('View More')}
          </Button.Ripple>
        </div>
        <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
          <ModalHeader>{t('Internal Attacks')}</ModalHeader>
          <ModalBody>
            <Table striped responsive>
              <thead>
                <tr>
                  <th>{t('Internal Attacks')}</th>
                  <th>{t('Counts')}</th>
                  <th>{t('Action')}</th>
                </tr>
              </thead>
              <tbody>
                {(shortTableData.length === 0 || checkApiData === false) ? (
                  <tr>
                    <td colSpan={3} className='text-center'>{t('Data Not Found')}</td>
                  </tr>
                ) : (
                  shortTableData.map((rows, index) => {
                    return (
                      <tr key={index}>
                        <td>
                          <span className='align-middle fw-bold'>{rows.threat_name}</span>
                        </td>
                        <td>
                          <span className='align-middle fw-bold'>{rows.threat_count}</span>
                        </td>
                        <td>
                          <Link to={`/nids-alert-internal-compromised-details?current_time=${rows.current_time}&past_time=${rows.past_time}&name=${rows.threat_name}`} className='btn-sm btn-outline-primary m-2'>
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
      <CardBody>
        {checkApiData ? (
          <Chart options={options} series={series} type='area' height={75} />
        ) : <DataNotFound />
        }
      </CardBody>
      {apiLoader ? <PreLoader /> : null}
    </Card>
  )
}

export default ActiveUsers
