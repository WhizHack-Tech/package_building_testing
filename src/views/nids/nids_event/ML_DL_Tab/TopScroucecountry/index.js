// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Events ML & DL ( Top Source Attacked Country )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { HorizontalBar } from 'react-chartjs-2'
import { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardBody, Table, CardSubtitle, Button, Modal, ModalHeader, ModalBody, Spinner } from 'reactstrap'
import axios from "@axios"
import { Link } from 'react-router-dom'
// import { Info} from 'react-feather'
import { useSelector } from "react-redux"
import { useTranslation } from 'react-i18next'
import { token } from '@utils'
import PreLoader from '../../preLoader'

const ChartjsBarChart = ({ tooltipShadow, gridLineColor, labelColor, successColorShade, lineChartPrimary, yellowColor }) => {
  const { t } = useTranslation()
  const [shortTableData, setTableData] = useState([])
  const [criticalThreatsTotal, setCriticalThreatsTotal] = useState(0)

  const [apiLoader, setApiLoader] = useState(false)
  const [modalBox, setModalBox] = useState(false)
  const filterState = useSelector((store) => store.dashboard_chart)

  const [checkApiData, setCheckApiData] = useState(true)

  const apiLogic = () => {

    setApiLoader(true)

    axios.get(`/cntry-bar-nids-event-ml?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)

        if (res.data.message_type === "d_not_f") {
          setCheckApiData(false)
        }

        if (res.data.message_type === "success") {
          setCheckApiData(true)
          setCriticalThreatsTotal(res.data.bar_chart)

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
    elements: {
      rectangle: {
        borderWidth: 2,
        borderSkipped: 'left',
        borderSkipped: 'top'
      }
    },
    responsive: true,
    maintainAspectRatio: false,
    responsiveAnimationDuration: 500,
    legend: {
      display: false
    },
    tooltips: {
      // Updated default tooltip UI
      shadowOffsetX: 1,
      shadowOffsetY: 1,
      shadowBlur: 8,
      shadowColor: tooltipShadow,
      backgroundColor: '#fff',
      titleFontColor: '#000',
      bodyFontColor: '#000'
    },
    // layout: {
    //   padding: {
    //     bottom: -30,
    //     left: -25
    //   }
    // },
    scales: {
      xAxes: [
        {
          display: true,
          gridLines: {
            zeroLineColor: gridLineColor,
            borderColor: 'transparent',
            color: gridLineColor,
            drawTicks: false
          },
          scaleLabel: {
            display: true,
            labelString: 'Count'
          },
          ticks: {
            fontColor: labelColor
          }
        }
      ],
      yAxes: [
        {
          display: true,
          gridLines: {
            display: false
          },
          scaleLabel: {
            display: true,
            labelString: 'Country'
          },
          ticks: {
            fontColor: labelColor
          }
        }
      ]
    }
  },
    data = {
      // labels: ['Routers', 'Laptops', 'Phones', 'Subnet', 'Servers', 'Dummy', 'Dummy'],
      labels: criticalThreatsTotal.labels,
      datasets: [
        {
          data: criticalThreatsTotal.series,
          backgroundColor: '#826bf8',
          borderColor: 'transparent',
          barThickness: 35
        }
      ]
    }


  return (
    <Card>
      <CardHeader className='d-flex justify-content-between align-items-sm-center align-items-start flex-sm-row flex-column'>
        <div>
          <CardTitle className='mb-75' tag='h4'>
            {t('Top Source Attack Countries')}
          </CardTitle>
        </div>
        <div className='round overflow-hidden round overflow-hidden'>
          <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
          {t('View More')}
          </Button.Ripple>
        </div>
        <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
          <ModalHeader> {t('Top Source Attack Countries')}</ModalHeader>
          <ModalBody>
            <Table striped responsive>
              <thead>
                <tr>
                  <th>{t('Top Source Attack Countries')}</th>
                  <th>{t('Platfrom')}</th>
                  <th>{t('Counts')}</th>
                  <th>{t('Actions')}</th>
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
                          <span className='align-middle fw-bold'>{rows.geoip_country_name}</span>
                        </td>
                        <td>
                          <span className='align-middle fw-bold'>{rows.platform}</span>
                        </td>
                        <td>
                          <span className='align-middle fw-bold'>{rows.geoip_country_name_count}</span>
                        </td>
                        <td>
                          <Link to={`/nids-events-ml-dl-counrty-details?current_time=${rows.current_time}&past_time=${rows.past_time}&geoip_country_name=${rows.geoip_country_name}&platform=${rows.platform}`} 
                          className='btn-sm btn-outline-primary m-2'
                          >
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
        {checkApiData ? (<div style={{ height: '350px' }}>
          <HorizontalBar data={data} options={options} height={300} />
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

export default ChartjsBarChart
