// ** Third Party Components
import { GoogleMap, useJsApiLoader, Marker, Circle } from '@react-google-maps/api'
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from '@axios'
import { useSelector } from 'react-redux'

// ** Reactstrap Imports
import { Card, CardHeader, CardTitle, CardBody, Table, CardSubtitle, Button, Modal, ModalHeader, ModalBody, Spinner } from 'reactstrap'

import PreLoader from '../preLoader'
import DataNotFound from '../dNotf'

const containerStyle = {
    width: '100%',
    height: '500px'
}

const center = {
    lat: 28.679079,
    lng: 77.069710
}

const GoogleMaps = () => {

    const [shortTableData, setTableData] = useState([])
    const [mapData, setMapData] = useState([])

    const [apiLoader, setApiLoader] = useState(false)
    const [modalBox, setModalBox] = useState(false)
    const filterState = useSelector((store => store.dashboard_chart))

    const { isLoaded } = useJsApiLoader({
        id: 'google-map-script',
        googleMapsApiKey: 'AIzaSyCYQSucAz2yP8li4efTQmlrA8WozVAfOuo'
    })

    const apiLogic = () => {
        setApiLoader(true)

        axios.get(`/nids-attck-event-geo?condition=${filterState.values ? filterState.values : 'today'}`)
            .then(res => {
                setApiLoader(false)
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
            <CardHeader className='border-bottom'>
                <CardTitle>
                    Map
                </CardTitle>

                <Button.Ripple color='primary' outline size='sm' onClick={() => setModalBox(!modalBox)}>
                    view More
                </Button.Ripple>

            </CardHeader>


            <Modal isOpen={modalBox} toggle={() => setModalBox(!modalBox)} size='lg'>
                <ModalHeader>Map</ModalHeader>
                <ModalBody>
                    <Table striped responsive>
                        <thead>
                            <tr>
                                <th>Countries</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                shortTableData.map((rows, index) => {
                                    return (
                                        <tr key={index}>
                                            <td>
                                                <span className='align-middle fw-bold'>{rows.title}</span>
                                            </td>
                                            <td>
                                                <Link to={`/map-details?current_time=${rows.current_time}&past_time=${rows.past_time}&name=${rows.title}`}>
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

            <CardBody className='mt-2'>
                {
                    isLoaded ? (
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
                    ) : <h4>Data Not Found</h4>
                }

            </CardBody>

            {apiLoader ? <PreLoader /> : null}
        </Card>
    )
}

export default GoogleMaps