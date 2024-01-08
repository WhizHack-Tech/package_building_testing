// ================================================================================================
//  File Name: Lisence.js
//  Description: Details of the Setting ( Edit Plan ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import { Card } from 'reactstrap'
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
