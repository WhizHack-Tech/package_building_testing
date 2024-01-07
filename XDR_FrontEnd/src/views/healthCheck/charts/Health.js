// ================================================================================================
//  File Name: Health.js
//  Description: Details of the Health Check ( Network Latency ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** React Imports
import { useEffect, useState } from 'react'

// ** Third Party Components
import axios from 'axios'
import Chart from 'react-apexcharts'

// ** Reactstrap Imports
import {
  Row,
  Col,
  Card,
  CardBody,
  CardText,
  CardTitle,
  CardHeader,
  DropdownMenu,
  DropdownItem,
  DropdownToggle,
  UncontrolledDropdown
} from 'reactstrap'

const SupportTracker = props => {
  // ** State
  const [data, setData] = useState(null)

  useEffect(() => {
    axios.get('/card/card-analytics/support-tracker').then(res => setData(res.data))
    return () => setData(null)
  }, [])

  const options = {
    plotOptions: {
      radialBar: {
        size: 150,
        offsetY: 10,
        startAngle: -150,
        endAngle: 150,
        hollow: {
          size: '70%'
        },
        track: {
          background: '#fff',
          strokeWidth: '50%'
        },
        dataLabels: {
          name: {
            offsetY: 20,
            fontFamily: 'Montserrat',
            fontSize: '1rem'
          },
          value: {
            offsetY: -15,
            fontFamily: 'Montserrat',
            fontSize: '1rem'
          }
        }
      }
    },
    colors: [props.danger],
    fill: {
      type: 'gradient',
      gradient: {
        shade: 'dark',
        type: 'horizontal',
        shadeIntensity: 0.5,
        gradientToColors: [props.primary],
        inverseColors: true,
        opacityFrom: 1,
        opacityTo: 1,
        stops: [0, 100]
      }
    },
    stroke: {
      dashArray: 8
    },

    labels: ['Network Latency']
  },

    series = [10]

  return data !== null ? (
    <Card>
      {/* <CardHeader>
      <CardTitle tag='h4'>Goal Overview</CardTitle>
    </CardHeader> */}
      <CardBody className='d-flex justify-content-center align-items-center'>
        <Chart options={options} series={series} type='radialBar' height={250} />
      </CardBody>
    </Card>
  ) : null
}
export default SupportTracker
