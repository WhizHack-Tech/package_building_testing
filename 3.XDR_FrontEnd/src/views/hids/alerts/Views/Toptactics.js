// ================================================================================================
//  File Name:  Topactics.js
//  Description: Details of the Top Actics Alert Graph.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import Chart from 'react-apexcharts'
import { Card, CardHeader, CardTitle, CardBody, CardSubtitle } from 'reactstrap'
import { useTranslation } from 'react-i18next'
const ApexRadiarChart = ({ toptactics }) => {
  let dataSize = Object.keys(toptactics).length
  const { t } = useTranslation()
  const options = {
    chart: {
      zoom: {
        enabled: false
      },
      parentHeightOffset: 0,
      toolbar: {
        show: true
      }
    },
    legend: {
      show: true,
      position: 'bottom'
    },
    labels: (dataSize > 0) ? toptactics.labels : [],

    colors: ['#826bf8', '#21409F', '#01a14b', '#3EB489', '#F70D1A', '#2916F5', '#F0E68C', '#EDDA74', '#FFD801', '#F4A460', '#C2B280', '#C04000', '#FF6347'],
    dataLabels: {
      enabled: true,
      formatter(val, opt) {
        return `${parseInt(val)}`
      }
    },
    plotOptions: {
      pie: {
        donut: {
          labels: {
            show: false,
            name: {
              fontSize: '2rem',
              fontFamily: 'Montserrat'
            },
            value: {
              fontSize: '1rem',
              fontFamily: 'Montserrat',
              formatter(val) {
                return `${parseInt(val)}`
              }
            },
            total: {
              show: false,
              fontSize: '1rem',
              formatter(w) {
                return '31'
              }
            }
          }
        }
      }
    },
    responsive: [
      {
        breakpoint: 992,
        options: {
          chart: {
            height: 380
          },
          legend: {
            position: 'bottom'
          }
        }
      },
      {
        breakpoint: 576,
        options: {
          chart: {
            height: 320
          },
          plotOptions: {
            pie: {
              donut: {
                labels: {
                  show: true,
                  name: {
                    fontSize: '1.5rem'
                  },
                  value: {
                    fontSize: '1rem'
                  },
                  total: {
                    fontSize: '1.5rem'
                  }
                }
              }
            }
          }
        }
      }
    ]
  }

  return (
    <Card>
      <CardHeader>
        <div>
          <CardTitle className='mb-75' tag='h4'>
          {t('Mitre Att&ck Tactics')}
          </CardTitle>
        </div>
      </CardHeader>
      <CardBody>
      {(dataSize > 0) ? <Chart options={options} series={toptactics.series} type='donut' height={380}/> : <p className='text-center mt-5'>{t('Data Not Found')}</p>}
      </CardBody>
    </Card>
  )
}

export default ApexRadiarChart
