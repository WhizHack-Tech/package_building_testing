// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Alerts ML & DL ( Detected Threat Details )
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================

import { useState, useEffect, Fragment } from 'react'
import { Link } from 'react-router-dom'
import axios from '@axios'
import { useSelector } from 'react-redux'
import Avatar from '@components/avatar'
// import IdsImg from "../../../assets/images/svg/ids.svg"
import IdsImg from '../../../../../assets/images/svg/ids.svg'
import DlImg from '../../../../../assets/images/svg/dl.svg'
import MlImg from '../../../../../assets/images/svg/ml.svg'
import { token } from '@utils'
import DataNotFound from '../../dNotf'
import { useTranslation } from 'react-i18next'
// ** Reactstrap Imports
import {
    Card, CardHeader, CardTitle, CardBody, Table, TabContent,
    TabPane,
    Nav,
    NavItem,
    Media,
    NavLink, Button, Modal, ModalHeader, ModalBody
} from 'reactstrap'

import PreLoader from '../../preLoader'

const DetectedThreatType = () => {
    const {t} = useTranslation()
    const [active, setActive] = useState('1')
    const [threatData, setThreatData] = useState({
        ml: [],
        dl: []
    })
    const [apiLoader, setApiLoader] = useState(false)
    const [modalBox, setModalBox] = useState(false)
    const filterState = useSelector((store => store.dashboard_chart))


    const apiLogic = () => {
        setApiLoader(true)

        axios.get(`/nids-alert-ml-detected-threat?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
            .then(res => {
                setApiLoader(false)

                if (res.data.message_type === "d_not_f") {
                    setThreatData({
                        ml: [],
                        dl: []
                    })
                }

                if (res.data.message_type === "success") {

                    setThreatData({
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

        return <DataNotFound />
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

        return <DataNotFound />
    }

    const ModalTableRender = ({ tableData, type }) => {

        return <Fragment>
            <ModalHeader>{t('Threat Types')}</ModalHeader>
            <Table striped responsive className='mt-2'>
                <thead>
                    <tr>
                        <th>{t('Threats Type')}</th>
                        <th>{t('Platform')}</th>
                        <th>{t('Counts')}</th>
                        <th>{t('Actions')}</th>
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
                                        <span className='align-middle fw-bold'>{rows.platform}</span>
                                    </td>
                                    <td>
                                        <span className='align-middle fw-bold'>{rows.value}</span>
                                    </td>
                                    <td>
                                        <Link to={`/nids-alert-ml-dl-details?current_time=${rows.current_time}&past_time=${rows.past_time}&type=${type}&name=${rows.name}&platform=${rows.platform}`} className='btn-sm btn-outline-primary m-2'>
                                            More Details
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
                    {t('Detected Threat Type')}
                </CardTitle>

                <div className='round overflow-hidden round overflow-hidden'>
                    <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
                    {t('View More')}
                    </Button.Ripple>
                </div>

            </CardHeader>


            <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='xl'>
                <ModalBody>
                    <TabContent className='py-50' activeTab={active}>
                        <TabPane tabId='1'>
                            <ModalTableRender type={'ml'} tableData={threatData.ml} />
                        </TabPane>
                        <TabPane tabId='2'>
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
                            {t('ML')}
                        </NavLink>
                    </NavItem>
                    <NavItem>
                        <NavLink
                            active={active === '2'}
                            onClick={() => {
                                toggle('2')
                            }}
                        >
                            {t('DL')}
                        </NavLink>
                    </NavItem>
                </Nav>
                <TabContent className='py-50' activeTab={active}>
                    <TabPane tabId='1'>
                        <Card className='card-transaction'>
                            <CardBody>
                                <MlRender />
                            </CardBody>
                        </Card>
                    </TabPane>
                    <TabPane tabId='2'>
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
