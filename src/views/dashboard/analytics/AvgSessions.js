import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from '@axios'
import { kFormatter } from '@utils'
import {
  Card,
  CardBody,
  CardText,
  Row,
  Col,
  Button,
  UncontrolledDropdown,
  DropdownMenu,
  DropdownItem,
  DropdownToggle,
  Progress
} from 'reactstrap'
import Chart from 'react-apexcharts'

const AvgSessions = props => {
  // const [data, setData] = useState(null)

  // useEffect(() => {
  //   axios.get('/card/card-analytics/avg-sessions').then(res => setData(res.data))
  // }, [])
  const [seriesdata, setSeriesData] = useState([])
  const [agentdata, setAgentData] = useState([])
  const [growthdata, setGrowthData] = useState([])
  const [growth_daysdata, setGrowth_daysData] = useState([])
  const [aws_agentdata, setAws_agentData] = useState([])
  const [azure_agentdata, setAzure_agentData] = useState([])
  const [gcp_agentdata, setGcp_agentData] = useState([])
  const [onprim_agentdata, setOnprim_agentData] = useState([])
  const [aws_valuedata, setAws_valueData] = useState([])
  const [azure_valuedata, setAzure_valueData] = useState([])
  const [gcp_valuedata, setGcp_valueData] = useState([])
  const [onprim_valuedata, setOnprim_valueData] = useState([])

  useEffect(() => {
    axios.get('/agent-platform-type-count').then((res) => {
      setSeriesData(res.data.series)
      setAgentData(res.data.agent)
      setGrowthData(res.data.growth)
      setGrowth_daysData(res.data.growth_days)
      setAws_agentData(res.data.aws_agent)
      setAzure_agentData(res.data.azure_agent)
      setGcp_agentData(res.data.gcp_agent)
      setOnprim_agentData(res.data.onprim_agent)
      setAws_valueData(res.data.aws_value)
      setAzure_valueData(res.data.azure_value)
      setGcp_valueData(res.data.gcp_value)
      setOnprim_valueData(res.data.onprim_value)
    })
  }, [])

  const options = {
      chart: {
        sparkline: { enabled: true },
        toolbar: { show: false }
      },
      grid: {
        show: false,
        padding: {
          left: 0,
          right: 0
        }
      },
      states: {
        hover: {
          filter: 'none'
        }
      },
       //colors: [props.primary, '#ebf0f7', '#ebf0f7', '#ebf0f7', '#ebf0f7', '#ebf0f7'],
       colors: [props.primary, props.warning, props.danger, props.success],
      plotOptions: {
        bar: {
          columnWidth: '45%',
          distributed: true,
          endingShape: 'rounded'
        }
      },
      tooltip: {
        x: { show: true }
      },
      xaxis: {
        type: 'numeric'
      }
    },
    series = [
      {
        name: 'Sessions',
        data: seriesdata
      }
    ]

  return (
    <Card>
      <CardBody>
        <Row className='pb-50'>
          <Col
            sm={{ size: 6, order: 1 }}
            xs={{ order: 2 }}
            className='d-flex justify-content-between flex-column mt-lg-0 mt-2'
          >
            <div className='session-info mb-1 mb-lg-0'>
            {/* <CardText className='font-weight-bold mb-2'>Total Agents</CardText> */}
              <h2 className='font-weight-bold mb-25'>Total {kFormatter(agentdata)} Agents</h2>
              <h5 className='font-medium-2'>
                <span className='text-success mr-50'>{growthdata}</span>
                <span className='font-weight-normal'>vs{growth_daysdata}</span>
              </h5>
            </div>
            <Button tag={Link} to={`/dashboard/agents`}color='primary'>View Details</Button>
          </Col>
          <Col
            sm={{ size: 6, order: 2 }}
            xs={{ order: 1 }}
            className='d-flex justify-content-between flex-column text-right'
          >
            {/* <UncontrolledDropdown className='chart-dropdown'>
              <DropdownToggle color='' className='bg-transparent btn-sm border-0 p-50'>
                Last 7 days
              </DropdownToggle>
              <DropdownMenu right>
                {data.last_days.map(item => (
                  <DropdownItem className='w-100' key={item}>
                    {item}
                  </DropdownItem>
                ))}
              </DropdownMenu>
            </UncontrolledDropdown> */}
            <Chart options={options} series={series} type='bar' height={200} />
          </Col>
        </Row>
        <hr />
        <Row className='pt-50'>
          <Col className='mb-2' md='6' sm='12'>
            <p className='mb-50'>AWS Agents: {aws_agentdata}</p>
            <Progress className='avg-session-progress mt-25' value={aws_valuedata} />
          </Col>
          <Col className='mb-2' md='6' sm='12'>
            <p className='mb-50'>Azure Agents: {kFormatter(azure_agentdata)}</p>
            <Progress className='avg-session-progress progress-bar-warning mt-25' value={azure_valuedata} />
          </Col>
          <Col md='6' sm='12'>
            <p className='mb-50'>GCP Agents: {gcp_agentdata}</p>
            <Progress className='avg-session-progress progress-bar-danger mt-25' value={gcp_valuedata} />
          </Col>
          <Col md='6' sm='12'>
            <p className='mb-50'>OnPrim Agents: {onprim_agentdata}</p>
            <Progress className='avg-session-progress progress-bar-success mt-25' value={onprim_valuedata} />
          </Col>
        </Row>
      </CardBody>
    </Card>
  )
}
export default AvgSessions
