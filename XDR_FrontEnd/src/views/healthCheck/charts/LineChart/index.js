// ================================================================================================
//  File Name: index.js
//  Description: Details of the Health Check.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { useState } from 'react'
import Chart from 'react-apexcharts'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { Card, CardHeader, CardText, CardBody, Table, Button, Modal, ModalHeader, ModalBody } from 'reactstrap'

const LineCharRender = ({ lineChart }) => {
  const { t } = useTranslation()
  const [modalBox, setModalBox] = useState(false)
  const { total, shortTableData, running, stop } = lineChart

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
      show: false
    },
    colors: ['#90EE90', '#FF0000'],
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
      name: t('Running'),
      data: running || []
    },
    {
      name: t('Stop'),
      data: stop || []
    }
  ]

  return (
    <Card>
      <CardHeader className='align-items-start pb-0'>
        <div>
          <h2 className='font-weight-bolder'>{total}</h2>
          <CardText>{t('Health Check Feeds')}</CardText>
        </div>
        <div className='round overflow-hidden round overflow-hidden'>
          <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
            {t('View More')}
          </Button.Ripple>
        </div>
        <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='xl'>
          <ModalHeader>{t('Health Check Feeds')}</ModalHeader>
          <ModalBody>
            <Table striped responsive>
              <thead>
                <tr>
                  <th>{t('Level')}</th>
                  <th>{t('Sensor ID')}</th>
                  <th>{t('Sensor Type')}</th>
                  <th>{t('Level Count')}</th>
                  <th>{t('Actions')}</th>
                </tr>
              </thead>
              <tbody>
                {
                  (shortTableData.length > 0) ? (
                    shortTableData.map((rows, index) => (
                      <tr key={index}>
                        <td>
                          <span className='align-middle fw-bold'>{rows.level}</span>
                        </td>

                        <td>
                          <span className='align-middle fw-bold'>{rows.sensor_id}</span>
                        </td>

                        <td>
                          <span className='align-middle fw-bold'>{rows.sensor_type}</span>
                        </td>

                        <td>
                          <span className='align-middle fw-bold'>{rows.level_count}</span>
                        </td>

                        <td>
                          <Link to={`/health-check/sensor-details?current_time=${rows.current_time}&past_time=${rows.past_time}&sensor_id=${rows.sensor_id}&sensor_type=${rows.sensor_type}&level=${rows.level}`} className='btn-sm btn-outline-primary m-2'>
                            {t('More Details')}
                          </Link>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={3} className='text-center'>{t('Data Not Found')}</td>
                    </tr>
                  )
                }
              </tbody>
            </Table>
          </ModalBody>
        </Modal>
      </CardHeader>
      <CardBody className="pb-2">
        {total > 0 ? (
          <Chart options={options} series={series} type='area' height={75} />
        ) : (
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
            <p>{t('Data Not Found')}</p>
          </div>
        )}
      </CardBody>
    </Card>
  )
}

export default LineCharRender
