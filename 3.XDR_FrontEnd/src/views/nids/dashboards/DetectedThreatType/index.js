import { useState, useEffect, Fragment } from 'react'
import { Link } from 'react-router-dom'
import axios from '@axios'
import { useSelector } from 'react-redux'
import Avatar from '@components/avatar'
import IdsImg from '../../../../assets/images/svg/ids.svg'
import DlImg from '../../../../assets/images/svg/dl.svg'
import MlImg from '../../../../assets/images/svg/ml.svg'

// ** Reactstrap Imports
import {
    Card, CardHeader, CardTitle, CardBody, Table, TabContent,
    TabPane,
    Nav,
    NavItem,
    Media,
    NavLink, Button, Modal, ModalHeader, ModalBody
} from 'reactstrap'

import PreLoader from '../preLoader'

const DetectedThreatType = () => {


    const [active, setActive] = useState('1')
    const [threatData, setThreatData] = useState({
        ids: [],
        ml: [],
        dl: []
    })

    const [apiLoader, setApiLoader] = useState(false)
    const [modalBox, setModalBox] = useState(false)
    const filterState = useSelector((store => store.dashboard_chart))


    const apiLogic = () => {
        setApiLoader(true)

        axios.get(`nids-dashboard-detected-threat-card?condition=${filterState.values ? filterState.values : 'last_1_hour'}`)
            .then(res => {
                setApiLoader(false)
                if (res.data.message_type === "success") {
                    setThreatData({
                        ids: res.data.detected_threat_type.ids,
                        ml: res.data.detected_threat_type.ml,
                        dl: res.data.detected_threat_type.dl
                    })
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

    const toggle = (tab) => {
        if (active !== tab) {
            setActive(tab)
        }
    }

    const IdsRender = () => {
        if (threatData.ids.length > 0) {
            return threatData.ids.map((item, key) => (
                <div className='transaction-item' key={key}>
                    <Media className="d-flex align-items-center">
                        <Avatar color='light-danger' icon={<img width={30} src={IdsImg} />} />
                        <Media body>
                            <h6 className='transaction-title'>{item?.name}</h6>
                        </Media>
                    </Media>
                    <div className={`font-weight-bolder ${item.down ? 'text-danger' : 'text-success'}`}>{item?.value}</div>
                </div>
            ))
        }

        return <h4 className='text-center mt-2'>Data Not Found</h4>
    }

    const MlRender = () => {
        if (threatData.ml.length > 0) {
            return threatData.ml.map((item, key) => (
                <div className='transaction-item' key={key}>
                    <Media className="d-flex align-items-center">
                        <Avatar color='light-primary' icon={<img width={30} src={MlImg} />} />
                        <Media body>
                            <h6 className='transaction-title'>{item?.name}</h6>
                        </Media>
                    </Media>
                    <div className={`font-weight-bolder ${item.down ? 'text-danger' : 'text-success'}`}>{item?.value}</div>
                </div>
            ))
        }

        return <h4 className='text-center mt-2'>Data Not Found</h4>
    }

    const DlRender = () => {
        if (threatData.dl.length > 0) {
            return threatData.dl.map((item, key) => (
                <div className='transaction-item' key={key}>
                    <Media className="d-flex align-items-center">
                        <Avatar color='light-info' icon={<img width={30} src={DlImg} />} />
                        <Media body>
                            <h6 className='transaction-title'>{item?.name}</h6>
                        </Media>
                    </Media>
                    <div className={`font-weight-bolder ${item.down ? 'text-danger' : 'text-success'}`}>{item?.value}</div>
                </div>
            ))
        }

        return <h4 className='text-center mt-2'>Data Not Found</h4>
    }

    const ModalTableRender = ({ tableData, type }) => {

        return <Fragment>
            <ModalHeader>Detected Threat Type : {type}</ModalHeader>
            <Table striped responsive className='mt-2'>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Counts</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        tableData.map((rows, index) => {
                            return (
                                <tr key={index}>
                                    <td>
                                        <span className='align-middle fw-bold'>{rows.name}</span>
                                    </td>
                                    <td>
                                        <span className='align-middle fw-bold'>{rows.value}</span>
                                    </td>
                                    <td>
                                        <Link to={`/detected-threat-details?current_time=${rows.current_time}&past_time=${rows.past_time}&type=${type}&name=${rows.name}`}>
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
        </Fragment>
    }

    return (
        <Card>
            <CardHeader>
                <CardTitle tag='h4'>
                    Detected Threat Type
                </CardTitle>

                <Button.Ripple color='primary' outline size='sm' onClick={() => setModalBox(!modalBox)}>
                    view More
                </Button.Ripple>

            </CardHeader>


            <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
                <ModalBody>
                    <TabContent className='py-50' activeTab={active}>
                        <TabPane tabId='1'>
                            <ModalTableRender type={'ids'} tableData={threatData.ids} />
                        </TabPane>
                        <TabPane tabId='2'>
                            <ModalTableRender type={'ml'} tableData={threatData.ml} />
                        </TabPane>
                        <TabPane tabId='3'>
                            <ModalTableRender type={'dl'} tableData={threatData.dl} />
                        </TabPane>
                    </TabContent>
                </ModalBody>
            </Modal>

            <CardBody>
                <Nav tabs justified>
                    <NavItem>
                        <NavLink
                            active={active === '1'}
                            onClick={() => {
                                toggle('1')
                            }}
                        >
                            IDS
                        </NavLink>
                    </NavItem>
                    <NavItem>
                        <NavLink
                            active={active === '2'}
                            onClick={() => {
                                toggle('2')
                            }}
                        >
                            ML
                        </NavLink>
                    </NavItem>
                    <NavItem>
                        <NavLink
                            active={active === '3'}
                            onClick={() => {
                                toggle('3')
                            }}
                        >
                            DL
                        </NavLink>
                    </NavItem>
                </Nav>
                <TabContent className='py-50' activeTab={active}>
                    <TabPane tabId='1'>
                        <Card className='card-transaction'>
                            <CardBody>
                                <IdsRender />
                            </CardBody>
                        </Card>
                    </TabPane>
                    <TabPane tabId='2'>
                        <Card className='card-transaction'>
                            <CardBody>
                                <MlRender />
                            </CardBody>
                        </Card>
                    </TabPane>
                    <TabPane tabId='3'>
                        <Card className='card-transaction'>
                            <CardBody>
                                <DlRender />
                            </CardBody>
                        </Card>
                    </TabPane>
                </TabContent>
            </CardBody>

            {apiLoader ? <PreLoader /> : null}
        </Card>
    )
}

export default DetectedThreatType
