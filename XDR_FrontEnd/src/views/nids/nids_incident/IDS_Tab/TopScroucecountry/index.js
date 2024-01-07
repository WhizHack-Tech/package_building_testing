// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Incidents IDS ( Top Source Attack Counties )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { HorizontalBar } from 'react-chartjs-2'
import { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardBody, Table, CardSubtitle, Button, Modal, ModalHeader, ModalBody, Spinner } from 'reactstrap'
import axios from "@axios"
import { Link } from 'react-router-dom'
import { Info } from 'react-feather'
import { useSelector } from "react-redux"
import { useTranslation } from 'react-i18next'
import { token } from '@utils'
import PreLoader from '../../preLoader'
import DataNotFound from '../../dNotf'
const ChartjsBarChart = ({ tooltipShadow, gridLineColor, labelColor, successColorShade, lineChartPrimary, yellowColor }) => {
  const { t } = useTranslation()
  const [shortTableData, setTableData] = useState([])
  const [countriesTotal, setCountriesTotal] = useState(0)

  const [apiLoader, setApiLoader] = useState(false)
  const [modalBox, setModalBox] = useState(false)
  const filterState = useSelector((store) => store.incident_charts)
  const [checkApiData, setCheckApiData] = useState(true)

  const apiLogic = () => {

    setApiLoader(true)

    axios.get(`/nids-incident-country-bar-chart?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
      .then(res => {
        setApiLoader(false)

        if (res.data.message_type === "d_not_f") {
          setCheckApiData(false)
        }

        if (res.data.message_type === "success") {
          setCheckApiData(true)
          setCountriesTotal(res.data.bar_chart)
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
        borderSkipped: 'bottom'
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
    scales: {
      xAxes: [
        {
          display: true,
          gridLines: {
            display: true,
            color: gridLineColor,
            zeroLineColor: gridLineColor
          },
          scaleLabel: {
            display: true,
            labelString: 'count'
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
            color: gridLineColor,
            zeroLineColor: gridLineColor
          },
          scaleLabel: {
            display: true,
            labelString: 'Countries'
          },
          ticks: {
            //stepSize: 1000,
            //  min: 0,
            // max: 400
            fontColor: labelColor
          }
        }
      ]
    }
  },
    data = {
      // labels: ['Routers', 'Laptops', 'Phones', 'Subnet', 'Servers', 'Dummy', 'Dummy'],
      labels: countriesTotal.labels,
      datasets: [
        {
          data: countriesTotal.series,
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
          <ModalHeader>{t('Top Source Attack Countries')}</ModalHeader>
          <ModalBody>
            <Table striped responsive>
              <thead>
                <tr>
                  <th>{t('Top Source Attack Countries')}</th>
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
                            <Link to={`/nids-incident-ids-countries-details?current_time=${rows.current_time}&past_time=${rows.past_time}&geoip_country_name=${rows.geoip_country_name}&platform=${rows.platform}`} className='btn-sm btn-outline-primary m-2'>
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
        <div style={{ height: '350px' }}>
          {checkApiData ? (
            <HorizontalBar data={data} options={options} height={300} />
          ) : (
            <DataNotFound />
          )}
        </div>
      </CardBody>

      {apiLoader ? <PreLoader /> : null}
    </Card>
  )
}

export default ChartjsBarChart
