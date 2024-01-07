import classnames from 'classnames'
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from '@axios'
import { useSelector } from 'react-redux'
import Avatar from '@components/avatar'
import { TrendingUp, User, Box, DollarSign } from 'react-feather'
import { Card, CardHeader, CardTitle, CardBody, CardText, Row, Col, Modal, ModalHeader, ModalBody, Button, Table, Media } from 'reactstrap'
import MlImg from '../../../../assets/images/svg/ml.svg'
import PreLoader from '../preLoader'
const StatsCard = ({ cols }) => {
  const [shortTableData, setTableData] = useState([])
  const [data, setData] = useState(0)

  const [apiLoader, setApiLoader] = useState(false)
  const [modalBox, setModalBox] = useState(false)
  const filterState = useSelector((store) => store.dashboard_chart) 
  const apiLogic = () => {

      setApiLoader(true)

      axios.get(`/nids-attck-event-service-name?condition=${filterState.values ? filterState.values : 'today'}`)
          .then(res => {
              setApiLoader(false)
              if (res.data.message_type === "success") {
                    setData(res.data.top_attacked_services)
                    setTableData(res.data.filter)
              }
          })
          .catch(error => {
              setApiLoader(false)
              console.log(error.message)
          })


  }

  useEffect(() => {
      apiLogic()

  }, [filterState.values, filterState.refreshCount])

    const renderData = () => {
        if (data.length > 0) {
            return data.map((item, index) => {
                const margin = Object.keys(cols)
                return (
                  <Col
                    key={index}
                    {...cols}
                    className={classnames({
                      [`mb-2 mb-${margin[0]}-0`]: index !== data.length - 1
                    })}
                  >
                    <Media>
                    <Avatar color='light-primary' icon={<img width={30} src={MlImg} />} className='mr-2'/>
                      <Media className='my-auto' body>
                        <h4 className='font-weight-bolder mb-0'>{item.name}</h4>
                        <CardText className='font-weight-bolder mb-0'>{item.val}</CardText>
                      </Media>
                    </Media>
                  </Col>
                )
              })
        }

        return <h4 className='text-center mt-2'>Data Not Found.</h4>
    }

    return (
        <Card className='card-statistics'>
            <CardHeader>
                <CardTitle tag='h4'>Top Attacked Services</CardTitle>
                <div>
                <Button.Ripple color='primary' outline size='sm' onClick={() => setModalBox(!modalBox)}>
                    view More
                </Button.Ripple>
                </div>
            </CardHeader>
            <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
                <ModalHeader>Top Attacked Services</ModalHeader>
                <ModalBody>
                    <Table striped responsive>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Counts</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                shortTableData.map((rows, index) => {
                                    return (
                                        <tr key={index}>
                                            <td>
                                                <span className='align-middle fw-bold'>{rows.name}</span>
                                            </td>
                                            <td>
                                                <span className='align-middle fw-bold'>{rows.val}</span>
                                            </td>
                                            <td>
                                                <Link to={`/top-services-details?current_time=${rows.current_time}&past_time=${rows.past_time}&name=${rows.name}`}>
                                                    <Button.Ripple color='primary' outline size='sm'>
                                                        More Details
                                                    </Button.Ripple>
                                                </Link>
                                            </td>
                                        </tr>
                                    )
                                })
                            }
                        </tbody>
                    </Table>
                </ModalBody>
            </Modal>
            <CardBody className='statistics-body'>
                <Row>{renderData()}</Row>
            </CardBody>

            {apiLoader ? <PreLoader /> : null}
        </Card>
    )
}

export default StatsCard
