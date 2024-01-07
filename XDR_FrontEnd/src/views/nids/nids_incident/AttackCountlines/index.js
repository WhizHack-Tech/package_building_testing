// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Incidents ( Attack Count Details )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==========================================================================================
import Chart from 'react-apexcharts'
import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { Info } from 'react-feather'
import { Card, CardHeader, CardText, CardBody, Table, CardSubtitle, Button, Modal, ModalHeader, ModalBody, Spinner } from 'reactstrap'
import { useSelector } from "react-redux"
import axios from '@axios'
import { token } from '@utils'
import PreLoader from '../preLoader'
const ApexLineChart = ({ direction, warning }) => {
  const { t } = useTranslation()
  const [shortTableData, setTableData] = useState([])
  const [criticalThreatsTotal, setCriticalThreatsTotal] = useState(0)

  const [apiLoader, setApiLoader] = useState(false)
  const [modalBox, setModalBox] = useState(false)
  const filterState = useSelector((store) => store.incident_charts)
  const [checkApiData, setCheckApiData] = useState(true)

  const apiLogic = () => {

    setApiLoader(true)

    axios.get(`/nids-incident-attack-freq?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)

        if (res.data.message_type === "d_not_f") {
          setCheckApiData(false)
        }

        if (res.data.message_type === "success") {
          setCheckApiData(true)
          setCriticalThreatsTotal(res.data.attack_frequency)
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
      zoom: {
        enabled: true
      },
      parentHeightOffset: 0,
      toolbar: {
        show: false
      }
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      show: true,
      curve: 'smooth'
    },
    grid: {
      xaxis: {
        lines: {
          show: true
        }
      },
      yaxis: {
        lines: {
          show: false
        }
      }
    },
    tooltip: {
      custom(data) {
        return `<div class='px-1 py-50'>
              <span>${data.series[data.seriesIndex][data.dataPointIndex]}</span>
            </div>`
      }
    },
    xaxis: {
      categories: criticalThreatsTotal.categories,
      scaleLabel: {
        display: true,
        labelString: 'Dates'
      }
    },
    yaxis: {
      opposite: direction === 'rtl'
    }
  }

  const series = [
    {
      data: criticalThreatsTotal.series
    }
  ]
  return (
    <Card>
      <CardHeader className='align-items-start pb-0'>
        <div>
          <h2 className='font-weight-bolder'>{criticalThreatsTotal.total}</h2>
          <CardText>{t('Attack Frequency')}</CardText>
        </div>
        <div className='round overflow-hidden round overflow-hidden'>
          <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
            {t('View More')}
          </Button.Ripple>
        </div>
        <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
          <ModalHeader>{t('Attack Frequency')}</ModalHeader>
          <ModalBody>
            <Table striped responsive>
              <thead>
                <tr>
                  <th>{t('Attack Frequency')}</th>
                  <th>{t('Counts')}</th>
                  <th>{t('Action')}</th>
                </tr>
              </thead>
              <tbody>
                {(shortTableData.length === 0 || checkApiData === false) ? (
                  <tr>
                    <td colSpan={3} className='text-center'>Data Not Found</td>
                  </tr>
                ) : (
                  shortTableData.map((rows, index) => {
                    return (
                      <tr key={index}>
                        <td>
                          <span className='align-middle fw-bold'>{rows.name}</span>
                        </td>
                        <td>
                          <span className='align-middle fw-bold'>{rows.val}</span>
                        </td>
                        <td>
                          <Link to={`/nids-incident-frequency-details/?current_time=${rows.current_time}&past_time=${rows.past_time}&name=${rows.name}`} className='btn-sm btn-outline-primary m-2'>
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
          <Chart options={options} series={series} type='area' height={250} />
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

export default ApexLineChart
