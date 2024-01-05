import { Fragment, useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardBody, CardSubtitle, Popover, PopoverHeader, PopoverBody, Badge } from 'reactstrap'
import { Circle, CircleMarker, Map, Marker, Polygon, Popup, Rectangle, TileLayer, Tooltip } from 'react-leaflet'
import axios from "axios"
import { Link } from 'react-router-dom'
import { Info} from 'react-feather'
import { useTranslation } from 'react-i18next'
import { useSelector } from "react-redux"

const MyPopupMarker = ({ position, content }) => (
  
  <Marker position={position}>
    <Popup>{content}</Popup>
    <CircleMarker center={position} color='red' radius={20}>
            {/* <Tooltip>Tooltip for CircleMarker</Tooltip> */}
          </CircleMarker>
  </Marker>
)

const MyMarkersList = ({ markers }) => {
  const items = markers.map(({ key, ...props }, keys) => <MyPopupMarker key={keys} {...props} />)
  return <Fragment>{items}</Fragment>
}

const MapMarkerList = () => {
  const {t} = useTranslation()
  const [popoverOpen, setPopoverOpen] = useState(false)
  const chart_data = useSelector((store) => store.attack_evnets_charts.charts)
  const chart_length = Object.keys(chart_data).length
  // const [markers, setMarkers] = useState([])

let markers = [] 
   
    if (chart_length > 0) {
      markers = chart_data.AttackerLocationsTimestamp
    }
   

  return (
    <Card>
      <CardHeader>
          <div>
            <CardTitle className='mb-75' tag='h4'>
            {t('Attacker Geo-Locations')}</CardTitle>
          </div>
          <Badge color='primary'>
            <Link><Info id='Attacker_Locations' size={20} /></Link>
          </Badge>
          <Popover
              placement='top'
              target='Attacker_Locations'
              isOpen={popoverOpen}
              toggle={() => setPopoverOpen(!popoverOpen)}
            >
              <PopoverHeader>{t('Attacker Geo-Locations')}</PopoverHeader>
            <PopoverBody>
                {t('Geo-Locations of the Top attackers')}</PopoverBody>
          </Popover>
      </CardHeader>
      <CardBody>
          <div style={{ height: '350px' }}>
              <Map style={{ height: '320px' }} center={[31.505, 40.09]} zoom={2.35} className='leaflet-map'>
                <TileLayer
                // attribution='<a >OpenStreetMap</a> '
                url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
                />
                <MyMarkersList markers={markers} />
              </Map>
            </div>
      </CardBody>
    </Card>
  )
}
export default MapMarkerList
