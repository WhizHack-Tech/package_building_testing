// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Incidents IDS ( Attacker IPs's )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import React, { useState, useEffect } from 'react'
import axios from '@axios'
import { Link } from 'react-router-dom'
import { Card, CardHeader, CardTitle, CardBody, Button, Modal, ModalHeader, ModalBody, Table } from 'reactstrap'
import { Bar } from 'react-chartjs-2'
import PreLoader from '../../preLoader'
import DataNotFound from '../../dNotf'
import { useSelector } from 'react-redux'
import { useTranslation } from 'react-i18next'
const ChartjsBarChart = ({ tooltipShadow, gridLineColor, labelColor, successColorShade, lineChartPrimary, yellowColor }) => {
  const [chartData, setChartData] = useState({
    options: {},
    series: [],
    isData: false
  })
  const {t} = useTranslation()
  const [shortTableData, setTableData] = useState([])
  const [apiLoader, setApiLoader] = useState(false)
  const filterState = useSelector((store) => store.incident_charts)
  const [modalBox, setModalBox] = useState(false)
  const [canvasOpen, setCanvasOpen] = useState(false)

  const ChartApiLogic = () => {
    setApiLoader(true)  

    axios
      .get(`/nids-attck-event-source-country?condition=${filterState.values ? filterState.values : 'last_1_hour'}`)
      .then((res) => {
        setApiLoader(false)
        if (res.data.message_type === 'success') {
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
                    color: gridLineColor,
                    zeroLineColor: gridLineColor
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
          }

          const chart = {
            labels: res.data.top_countries.labels,
            datasets: [
              {
                data: res.data.top_countries.series,
                backgroundColor: '#666ee8',
                borderColor: 'transparent',
                barThickness: 35
              }
            ]
          }

          setChartData(pre => ({...pre, isData: true, options, series: chart}))

          // Update the table data
          if (res.data.top_countries.series.length > 0) {
            const tableDataRows = res.data.top_countries.series.map((series, index) => ({
              series,
              labels: res.data.top_countries.labels[index],
              past_time: res.data.filter.past_time,
              current_time: res.data.filter.current_time
            }))

            setTableData(tableDataRows)
          }
        }
      })
      .catch((error) => {
        setApiLoader(false)
        console.log(error.message)
      })
  }

  useEffect(() => {
    ChartApiLogic()
  }, [filterState.values, filterState.refreshCount])

  return (
    <Card>
      <CardHeader className="d-flex justify-content-between align-items-sm-center align-items-start flex-sm-row flex-column">
      <div>
        <CardTitle className='mb-75' tag='h4'>{t('Attacker IPs')}</CardTitle>
      </div>
        <Button.Ripple color="primary" outline size="sm" onClick={() => setModalBox(!modalBox)}>
          {t('View More')}
        </Button.Ripple>
      </CardHeader>
      <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size="lg">
        <ModalHeader>{t('Attacker IPs')}</ModalHeader>
        <ModalBody>
        <Table striped responsive>
  <thead>
    <tr>
      <th>{t('Attacker IPs')}</th>
      <th>{t('Counts')}</th>
      <th>{t('Action')}</th>
    </tr>
  </thead>
  <tbody>
    {shortTableData.map((row, index) => {
      return (
        <tr key={index}>
          <td>
            <span className="align-middle fw-bold">{row.series}</span>
          </td>
          <td>
            <span className="align-middle fw-bold">{row.labels}</span>
          </td>
          <td>
            <Link
              to={`/top-attacked-countries-details?current_time=${row.current_time}&past_time=${row.past_time}&name=${row.labels}`}
            >
              <Button.Ripple color="primary" outline size="sm">
                {t('More Details')}
              </Button.Ripple>
            </Link>
          </td>
        </tr>
      )
    })}
  </tbody>
</Table>

        </ModalBody>
      </Modal>
      <CardBody>
        <div style={{ height: '300px'}}>
          {chartData.isData ? (
            <Bar options={chartData.options} data={chartData.series} height={280} />
          ) : (
            <DataNotFound />
          )}
        </div>
      </CardBody>
      {apiLoader && <PreLoader />}
    </Card>
  )
}

export default ChartjsBarChart