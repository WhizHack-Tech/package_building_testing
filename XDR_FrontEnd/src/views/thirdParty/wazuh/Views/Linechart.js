import Chart from 'react-apexcharts'
import { useTranslation } from 'react-i18next'
import { Card, CardHeader, CardTitle, CardBody } from 'reactstrap'

const ApexLineChart = ({alert_Groups}) => {
  const {t} = useTranslation()
  const alertGroupsLength = Object.keys(alert_Groups).length
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
    labels: (alertGroupsLength > 0) ? alert_Groups.labels : [],
    colors: ['#ffe700', '#00d4bd', '#826bf8', '#2b9bf4', '#FFA1A1', '#008000', '#f70d1a'],
    xaxis: {
    }
  }
 

  return (
    <Card>
      <CardHeader className='d-flex flex-sm-row flex-column justify-content-md-between align-items-start justify-content-start'>
        <div>
          <CardTitle className='mb-75' tag='h4'>
            {t('Alert Groups Evolution')}
          </CardTitle>
          {/* <CardSubtitle className='text-muted'>IP Attacks</CardSubtitle> */}
        </div>
      </CardHeader>
      <CardBody>
        {(alertGroupsLength > 0) ? <Chart options={options} series={alert_Groups.series} type='line' height={350} />  : <p className='text-center mt-5'>{t('Data Not Found')}</p>}
        
      </CardBody>
    </Card>
  )
}

export default ApexLineChart
