import { useEffect, useState } from 'react'
import classnames from 'classnames'
import axios from '@axios'
import {
  Card,
  CardHeader,
  CardTitle,
  CardBody,
  UncontrolledDropdown,
  DropdownMenu,
  DropdownItem,
  DropdownToggle
} from 'reactstrap'
// import * as Icon from 'react-feather'
import { Monitor, Tablet, ArrowDown, ArrowUp, Circle } from 'react-feather'
import Chart from 'react-apexcharts'

const Customers = props => {
  // const [data, setData] = useState(null)

  // useEffect(() => {
  //   axios.get('/card/card-analytics/customers').then(res => setData(res.data))
  // }, [])

  const [seriesdata, setseriesData] = useState([])
  const [new_countdata, setNew_countData] = useState([])
  const [returning_countdata, setReturning_countData] = useState([])
  const [referrals_countdata, setreferrals_countData] = useState([])

  useEffect(() => {
    axios.get('/customers').then((res) => {
      setseriesData(res.data.series)
      setNew_countData(res.data.new_count)
      setReturning_countData(res.data.returning_count)
      setreferrals_countData(res.data.referrals_count)
    })
  }, [])

  const options = {
      chart: {
        toolbar: {
          show: false
        }
      },
      labels: ['New', 'Returning', 'Referrals'],
      dataLabels: {
        enabled: true
      },
      legend: { show: false },
      stroke: {
        width: 4
      },
      colors: [props.primary, props.warning, props.danger]
    },
    series = seriesdata

  const renderChartInfo = () => {
    return data.listData.map((item, index) => {
      const IconTag = Icon[item.icon]

      return (
        <div
          key={index}
          className={classnames('d-flex justify-content-between', {
            'mb-1': index !== data.listData.length - 1
          })}
        >
          <div className='d-flex align-items-center'>
            <IconTag
              size={15}
              className={classnames({
                [item.iconColor]: item.iconColor
              })}
            />
            <span className='font-weight-bold ml-75'>{item.text}</span>
          </div>
          <span>{item.result}</span>
        </div>
      )
    })
  }

  return (
    <Card>
      <CardHeader className='align-items-end'>
        <CardTitle tag='h4'>Customers</CardTitle>
        <UncontrolledDropdown className='chart-dropdown'>
          {/* <DropdownToggle color='' className='bg-transparent btn-sm border-0 p-50'>
            Last 7 days
          </DropdownToggle> */}
          {/* <DropdownMenu right>
            {data.last_days.map(item => (
              <DropdownItem className='w-100' key={item}>
                {item}
              </DropdownItem>
            ))}
          </DropdownMenu> */}
        </UncontrolledDropdown>
      </CardHeader>
      <CardBody>
        <Chart options={options} series={series} type='pie' height={325} />
        {/* <div className='pt-25'>{renderChartInfo()}</div> */}
        <div className='d-flex justify-content-between mt-1 mb-1'>
          <div className='d-flex align-items-center'>
            <Circle size={17} className='text-primary' />
            <span className='font-weight-bold ml-75 mr-25'>New</span>
            {/* <span>- 39%</span> */}
          </div>
          <div>
            <span>{new_countdata}</span>
          </div>
        </div>
        <div className='d-flex justify-content-between mt-1 mb-1'>
          <div className='d-flex align-items-center'>
            <Circle size={17} className='text-warning' />
            <span className='font-weight-bold ml-75 mr-25'>Returning</span>
            {/* <span>- 39%</span> */}
          </div>
          <div>
            <span>{returning_countdata}</span>
          </div>
        </div>
        <div className='d-flex justify-content-between mt-1 mb-1'>
          <div className='d-flex align-items-center'>
            <Circle size={17} className='text-Danger' />
            <span className='font-weight-bold ml-75 mr-25'>Referrals</span>
            {/* <span>- 39%</span> */}
          </div>
          <div>
            <span>{referrals_countdata}</span>
          </div>
        </div>
      </CardBody>
    </Card>
  ) 
}
export default Customers
