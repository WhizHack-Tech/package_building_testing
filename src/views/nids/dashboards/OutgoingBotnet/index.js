// ** Third Party Components
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from '@axios'
import { useSelector } from 'react-redux'
// import internal from "../../../../assets/images/svg/internal.svg"
import internal from "../../../../assets/images/svg/Critical.svg"
import Avatar from '@components/avatar'
// ** Reactstrap Imports
import { Card, CardHeader, CardTitle, CardBody, Table, CardSubtitle, Button, Modal, ModalHeader, ModalBody, Spinner } from 'reactstrap'

import PreLoader from '../preLoader'

const CriticalThreats = () => {

    const [shortTableData, setTableData] = useState([])
    const [outgoingThreatsTotal, setOutgoingThreatsTotal] = useState(0)

    const [apiLoader, setApiLoader] = useState(false)
    const [modalBox, setModalBox] = useState(false)
    const filterState = useSelector((store) => store.dashboard_chart) 
    const apiLogic = () => {

        setApiLoader(true)

        axios.get(`/nids-dashboard-outgoing-botnet?condition=${filterState.values ? filterState.values : 'today'}`)
            .then(res => {
                setApiLoader(false)
                if (res.data.message_type === "success") {
                    setOutgoingThreatsTotal(res.data.attack_count)
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
            <CardHeader tag='h4'>
                <CardTitle>
                Outgoing Botnet Connections
                </CardTitle>

                <Button.Ripple color='primary' outline size='sm' onClick={() => setModalBox(!modalBox)}>
                    view More
                </Button.Ripple>

            </CardHeader>


            <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
                <ModalHeader>Outgoing Botnet Connections</ModalHeader>
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
                                                <Link to={`/outgoing-botnet-details?current_time=${rows.current_time}&past_time=${rows.past_time}&name=${rows.threat_name}`}>
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
                <Avatar color='light-primary' icon={<img width={40} src={internal} />} size='lg'/>
                    <h1>{outgoingThreatsTotal}</h1>
                    <p>Internal Attack Count</p>
                </div>
            </CardBody>

            {apiLoader ? <PreLoader /> : null}
        </Card>
    )
}

export default CriticalThreats