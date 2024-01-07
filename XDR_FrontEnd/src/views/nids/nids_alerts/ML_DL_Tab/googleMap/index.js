// ================================================================================================
//  File Name: index.js
//  Description: Details of the NIDS Alerts ML & DL ( Geo Location )
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
import { Card, CardHeader, CardTitle, CardBody, Table, CardSubtitle, Button, Modal, ModalHeader, ModalBody, Spinner } from 'reactstrap'
import { useTranslation } from 'react-i18next'
import PreLoader from '../../preLoader'
import DataNotFound from '../../dNotf'

const containerStyle = {
    width: '100%',
    height: '500px'
}

const center = {
    lat: 28.679079,
    lng: 77.069710
}

const GoogleMaps = () => {
    const {t} = useTranslation()
    const [shortTableData, setTableData] = useState([])
    const [mapData, setMapData] = useState([])

    const [apiLoader, setApiLoader] = useState(false)
    const [modalBox, setModalBox] = useState(false)
    const filterState = useSelector((store => store.dashboard_chart))

    const { isLoaded } = useJsApiLoader({
        id: 'google-map-script',
        googleMapsApiKey: 'AIzaSyCA4umQW7x-Tlyws2aM0YlwZd18R5C_jso'
    })

    const apiLogic = () => {
        setApiLoader(true)

        axios.get(`/nids-alert-ml-map?condition=${filterState.values ? filterState.values : 'last_1_hour'}`, { headers: { Authorization: token() } })
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
            <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
                <ModalHeader>{t('Attacker Geo-Locations')}</ModalHeader>
                <ModalBody>
                    <Table striped responsive>
                        <thead>
                            <tr>
                                <th>{t('City Name')}</th>
                                <th>{t('Platform')}</th>
                                <th>{t('Count')}</th>
                                <th>{t('Action')}</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                shortTableData.map((rows, index) => {
                                    return (
                                        <tr key={index}>
                                            <td>
                                                <span className='align-middle fw-bold'>{rows.geoip_city}</span>
                                            </td>
                                            <td>
                                                <span className='align-middle fw-bold'>{rows.platform}</span>
                                            </td>
                                            <td>
                                                <span className='align-middle fw-bold'>{rows.geoip_city_count}</span>
                                            </td>
                                            <td>
                                                <Link to={`/nids-alert-ml-dl-geo-location-details?current_time=${rows.current_time}&past_time=${rows.past_time}&geoip_city=${rows.geoip_city}&platform=${rows.platform}`} className='btn-sm btn-outline-primary m-2'>
                                                   {t(' More Details')}
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