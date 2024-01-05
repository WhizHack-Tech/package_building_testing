import React, { useState, useEffect } from 'react'
import axios from '@axios'
import { Link } from 'react-router-dom'
import { Card, CardHeader, CardTitle, CardBody, Button, Modal, ModalHeader, ModalBody, Table } from 'reactstrap'
import { HorizontalBar } from 'react-chartjs-2'
import PreLoader from '../preLoader'
import DataNotFound from '../dNotf'
import { useSelector } from 'react-redux'

const ChartjsBarChart = ({ tooltipShadow, gridLineColor, labelColor }) => {
  const [chartData, setChartData] = useState({
    options: {},
    series: []
  })
  const [shortTableData, setTableData] = useState([])
  const [apiLoader, setApiLoader] = useState(false)
  const filterState = useSelector((store) => store.dashboard_chart)
  const [modalBox, setModalBox] = useState(false)
  const [canvasOpen, setCanvasOpen] = useState(false)

  const ChartApiLogic = () => {
    setApiLoader(true)

    axios
      .get(`/nids-attck-event-source-country?condition=${filterState.values ? filterState.values : 'today'}`)
      .then((res) => {
        setApiLoader(false)
        if (res.data.message_type === 'success') {
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
          }

          const chart = {
            labels: res.data.top_countries.labels,
            datasets: [
              {
                data: res.data.top_countries.series,
                backgroundColor: '#80a5ec',
                borderColor: 'transparent',
                barThickness: 30
              }
            ]
          }

          setChartData({
            options,
            series: chart
          })

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
        <CardTitle tag="h4">Top Source Attack Countries</CardTitle>
        <Button.Ripple color="primary" outline size="sm" onClick={() => setModalBox(!modalBox)}>
          View More
        </Button.Ripple>
      </CardHeader>
      <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size="lg">
        <ModalHeader>Top Source Attack Countries</ModalHeader>
        <ModalBody>
        <Table striped responsive>
  <thead>
    <tr>
      <th>Countries</th>
      <th>Counts</th>
      <th>Action</th>
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
                More Details
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
        <div style={{ height: '400px' }}>
          {chartData.series ? (
            <HorizontalBar options={chartData.options} data={chartData.series} height={300} />
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
