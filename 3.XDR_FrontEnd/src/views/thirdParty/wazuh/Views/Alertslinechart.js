import Chart from 'react-apexcharts'
import { useTranslation } from 'react-i18next'
import { Card, CardHeader, CardTitle, CardBody } from 'reactstrap'

const ApexLineChart = ({alerts_evolution}) => {
  const {t} = useTranslation()
  const alertDataLength = Object.keys(alerts_evolution).length
  
  const options = {
    chart: {
      height: 300,
      type: 'line',
      zoom: {
        enabled: true
      },
      animations: {
        enabled: true
      }
    },
    stroke: {
      width: [5, 5, 5, 5, 5, 5, 5],
      curve: 'straight'
    },
    labels: (alertDataLength > 0) ? alerts_evolution.labels : [],
    colors: ['#ffe700', '#00d4bd', '#826bf8', '#2b9bf4', '#FFA1A1', '#008000', '#f70d1a'],
    xaxis: {
    }
  }
 

  return (
    <Card>
      <CardHeader className='d-flex flex-sm-row flex-column justify-content-md-between align-items-start justify-content-start'>
        <div>
          <CardTitle className='mb-75' tag='h4'>
            {t('Mitra Alerts Evolution Over Time')}
          </CardTitle>
          {/* <CardSubtitle className='text-muted'>IP Attacks</CardSubtitle> */}
        </div>
      </CardHeader>
      <CardBody>
        {(alertDataLength > 0) ? <Chart options={options} series={alerts_evolution.series} type='line' height={350} />  : <p className='text-center mt-5'>{t('Data Not Found')}</p>}
        
      </CardBody>
    </Card>
  )
}

export default ApexLineChart
