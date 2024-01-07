import Chart from 'react-apexcharts'
import { Card, CardHeader, CardTitle, CardBody, CardSubtitle } from 'reactstrap'
import { useTranslation } from 'react-i18next'
const ApexRadiarChart = ({ rule_attack }) => {
  let dataSize = Object.keys(rule_attack).length
  const {t} = useTranslation()
  const donutColors = {
    series1: '#ffe700',
    series2: '#00d4bd',
    series3: '#826bf8',
    series4: '#2b9bf4',
    series5: '#FFA1A1'
  }
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
    labels: (dataSize > 0) ? rule_attack.labels : [],

    colors: [donutColors.series1, donutColors.series5, donutColors.series3, donutColors.series2],
    dataLabels: {
      enabled: true,
      formatter(val, opt) {
        return `${parseInt(val)}%`
      }
    },
    plotOptions: {
      pie: {
        donut: {
          labels: {
            show: true,
            name: {
              fontSize: '2rem',
              fontFamily: 'Montserrat'
            },
            value: {
              fontSize: '1rem',
              fontFamily: 'Montserrat',
              formatter(val) {
                return `${parseInt(val)}%`
              }
            },
            total: {
              show: false,
              fontSize: '1rem',
              formatter(w) {
                return '31%'
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
          {t('Rule Level By Attack ID')}
          </CardTitle>
        </div>
      </CardHeader>
      <CardBody>
      {(dataSize > 0) ? <Chart options={options} series={rule_attack.series} type='donut' height={380}/> : <p className='text-center mt-5'>{t('Data Not Found')}</p>}
      </CardBody>
    </Card>
  )
}

export default ApexRadiarChart
