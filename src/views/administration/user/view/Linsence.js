// ================================================================================================
//  File Name: ApiKey.js
//  Description: Details of the Administration ( View Organization Details ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// ===========================================================================================
import { Card } from 'reactstrap'
import "./Loader.css"
import TraceLicense from './traceLicense'
import Nids from './Nidslisence'
import Hids from './Hisdlinsence'
import SoarSensor from './SoarSensor'

const Lisence = () => {
  return (
    <Card>
      <TraceLicense />
      <hr />
      <Nids />
      <hr />
      <Hids />
      <hr />
      <SoarSensor />
    </Card>
  )
}

export default Lisence
