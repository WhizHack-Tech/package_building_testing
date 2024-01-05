// ** Third Party Components
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from '@axios'
import { useSelector } from 'react-redux'
// import Critical from "../../../../assets/images/svg/Botnet.svg"
import Critical from "../../../../assets/images/svg/Botnet.svg"
import Avatar from '@components/avatar'
// ** Reactstrap Imports
import { Card, CardHeader, CardTitle, CardBody, Table, CardSubtitle, Button, Modal, ModalHeader, ModalBody, Spinner } from 'reactstrap'

import PreLoader from '../preLoader'

const CriticalThreats = () => {

    const [shortTableData, setTableData] = useState([])
    const [criticalThreatsTotal, setCriticalThreatsTotal] = useState(0)

    const [apiLoader, setApiLoader] = useState(false)
    const [modalBox, setModalBox] = useState(false)
    const filterState = useSelector((store) => store.dashboard_chart) 
    const apiLogic = () => {

        setApiLoader(true)

        axios.get(`nids-dashboard-critical-threats?condition=${filterState.values ? filterState.values : 'last_1_hour'}`)
            .then(res => {
                setApiLoader(false)
                if (res.data.message_type === "success") {
                    setCriticalThreatsTotal(res.data.critical_threat_total)
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

    return (
        <Card>
            <CardHeader>
                <CardTitle tag='h4'>
                    Critical Threats
                </CardTitle>
                <div>
                <Button.Ripple color='primary' outline size='sm' onClick={() => setModalBox(!modalBox)}>
                    view More
                </Button.Ripple>
                </div>
            </CardHeader>
            <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
                <ModalHeader>Critical Threats</ModalHeader>
                <ModalBody>
                    <Table striped responsive>
                        <thead>
                            <tr>
                                <th>Critical Threats Name</th>
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
                                                <span className='align-middle fw-bold'>{rows.threat_name}</span>
                                            </td>
                                            <td>
                                                <span className='align-middle fw-bold'>{rows.threat_count}</span>
                                            </td>
                                            <td>
                                                <Link to={`/critical-threats-details?current_time=${rows.current_time}&past_time=${rows.past_time}&name=${rows.threat_name}`}>
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

            <CardBody>
                <div className='text-center mt-2'>
                <Avatar color='light-info' icon={<img width={40} src={Critical} />} size='lg'/>
                    <h1>{criticalThreatsTotal}</h1>
                    <p>High Severity Events</p>
                </div>
            </CardBody>

            {apiLoader ? <PreLoader /> : null}
        </Card>
    )
}

export default CriticalThreats