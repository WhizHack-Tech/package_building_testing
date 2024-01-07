// ================================================================================================
//  File Name: index.js
//  Description: Details of the Trace ( Events ( Geo Location )).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** Third Party Components
import { GoogleMap, useJsApiLoader, Marker, Circle } from '@react-google-maps/api'
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from '@axios'
import { useSelector } from 'react-redux'
import { token } from '@utils'
// ** Reactstrap Imports
import { Card, CardHeader, CardTitle, CardBody, Table, Button, Modal, ModalHeader, ModalBody, Label, Col, Input, Row } from 'reactstrap'

import PreLoader from '../../preLoader'
import DataNotFound from '../../dNotf'
import { useTranslation } from 'react-i18next'

const containerStyle = {
    width: '100%',
    height: '500px'
}

const center = {
    lat: 28.679079,
    lng: 77.069710
}

const GoogleMaps = () => {
    const { t } = useTranslation()
    const [shortTableData, setTableData] = useState([])
    const [mapData, setMapData] = useState([])

    const [apiLoader, setApiLoader] = useState(false)
    const [modalBox, setModalBox] = useState(false)
    const filterState = useSelector((store => store.dashboard_chart))
    const [searchQuery, setSearchQuery] = useState('')

    const { isLoaded } = useJsApiLoader({
        id: 'google-map-script',
        googleMapsApiKey: 'AIzaSyCA4umQW7x-Tlyws2aM0YlwZd18R5C_jso'
    })

    const apiLogic = () => {
        setApiLoader(true)

        axios.get(`/geo-location-trace-event?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
            .then(res => {
                setApiLoader(false)

                if (res.data.message_type === "d_not_f") {
                    setTableData([])
                    setMapData([])
                }

                if (res.data.message_type === "success") {
                    setTableData(res.data.filter)
                    setMapData(res.data.geolocation)
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

    const filteredData = shortTableData.filter((rows) => rows.sensor_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        rows.geoip_city.toLowerCase().includes(searchQuery.toLowerCase())
    )

    return (
        <Card>
            <CardHeader>
                <CardTitle>
                    {t('Attacker Geo-Locations')}
                </CardTitle>
                <div className='round overflow-hidden round overflow-hidden'>
                    <Button.Ripple color='flat-primary' size='sm' onClick={() => setModalBox(!modalBox)}>
                        {t('View More')}
                    </Button.Ripple>
                </div>
            </CardHeader>
            <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='xl'>
                <ModalHeader>{t('Attacker Geo-Locations')}</ModalHeader>
                <Row className='justify-content-end mx-0'>
                    <Col className='d-flex align-items-center justify-content-end mt-1' md='6' sm='12'>
                        <Label className='mr-1' for='search-input'>
                            {t('Search')}
                        </Label>
                        <Input
                            className='dataTable-filter mb-50'
                            type='text'
                            bsSize='sm'
                            id='search-input'
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value.trim())}
                        />
                    </Col>
                </Row>
                <ModalBody>
                    <Table striped responsive>
                        <thead>
                            <tr>
                                <th>{t('Sensor Name')}</th>
                                <th>{t('City Name')}</th>
                                <th>{t('Count')}</th>
                                <th>{t('Actions')}</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                filteredData.map((rows, index) => {
                                    <tr>
                                        <td colSpan={3} className='text-center'>{t('Data Not Found')}</td>
                                    </tr>
                                    return (
                                        <tr key={index}>
                                            <td>
                                                <span className='align-middle fw-bold'>{rows.sensor_name}</span>
                                            </td>
                                            <td>
                                                <span className='align-middle fw-bold'>{rows.geoip_city}</span>
                                            </td>
                                            <td>
                                                <span className='align-middle fw-bold'>{rows.geoip_city_count}</span>
                                            </td>
                                            <td>
                                                <Link to={`/trace-events-geo-location-details?current_time=${rows.current_time}&past_time=${rows.past_time}&name=${rows.geoip_city}&name1=${rows.sensor_name}`} className='btn-sm btn-outline-primary m-2'>
                                                    {t('More Details')}
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

            <CardBody className='mt-2'>
                {
                    (isLoaded && mapData.length > 0) ? (
                        <GoogleMap
                            mapContainerStyle={containerStyle}
                            center={center}
                            zoom={3}
                        >
                            {mapData.map((data, key) => (
                                <Marker
                                    key={key}
                                    title={data.title}
                                    position={{ lat: data.position[1], lng: data.position[0] }}
                                />
                            ))}
                            {mapData.map((data, key) => (
                                <Circle
                                    key={key}
                                    center={{ lat: data.position[1], lng: data.position[0] }}
                                    radius={10000}
                                    options={{ strokeColor: '#FF0000' }}
                                />
                            ))}
                        </GoogleMap>
                    ) : <DataNotFound />
                }

            </CardBody>

            {apiLoader ? <PreLoader /> : null}
        </Card>
    )
}

export default GoogleMaps