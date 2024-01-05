import Chart from 'react-apexcharts'
import { Card, CardHeader, CardTitle, CardBody } from 'reactstrap'
import { useTranslation } from 'react-i18next'

const ApexColumnCharts = ({ direction, mitre_Attacks }) => {
    const {t} = useTranslation()
    const mitreGroupsLength = Object.keys(mitre_Attacks).length
    const options = {
        chart: {
            height: 400,
            type: 'bar',
            stacked: true,
            parentHeightOffset: 0,
            toolbar: {
                show: true
            }
        },
        plotOptions: {
            bar: {
                columnWidth: '15%',
                colors: {
                    backgroundBarColors: [],
                    backgroundBarRadius: 5
                }
            }
        },
        dataLabels: {
            enabled: false
        },
        legend: {
            position: 'top',
            horizontalAlign: 'start'
        },
        colors: ['#ffe700', '#00d4bd', '#826bf8', '#2b9bf4', '#FFA1A1', '#008000', '#f70d1a'],
        stroke: {
            show: true,
            colors: ['transparent']
        },
        grid: {
            xaxis: {
                lines: {
                    show: true
                }
            }
        },
        xaxis: {
            categories: (mitreGroupsLength > 0) ? mitre_Attacks.labels : []
        },
        fill: {
            opacity: 1
        },
        yaxis: {
            opposite: direction === 'rtl'
        }
    }

    return (
        <Card>
            <CardHeader className='d-flex flex-md-row flex-column justify-content-md-between justify-content-start align-items-md-center align-items-start'>
                <CardTitle tag='h4'>{t('MITRE Tactic Details')}</CardTitle>
            </CardHeader>
            <CardBody>
            {(mitreGroupsLength > 0) ? <Chart options={options} series={mitre_Attacks.series} type='bar' height={350} />  : <p className='text-center mt-5'>{t('Data Not Found')}</p>}
            </CardBody>
        </Card>
    )
}

export default ApexColumnCharts
