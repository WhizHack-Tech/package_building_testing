// ================================================================================================
//  File Name: index.js
//  Description: Details of the Setting ( Plan Add ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Master Dashboard
//  Author URL: https://whizhack.in
// =============================================================================================
import { Card, Button } from 'reactstrap'
import TraceLicense from './traceLicense'
import Nids from './Nidslisence'
import Hids from './Hisdlinsence'
import SoarSensor from './SoarSensor'
import { ArrowLeft, ArrowRight } from 'react-feather'
import { Link } from 'react-router-dom'

const Lisence = ({ stepper }) => {
    return (
        <Card>
            <TraceLicense />
            <hr />
            <Nids />
            <hr />
            <Hids />
            <hr />
            <SoarSensor />
            <hr />
            <div className='d-flex justify-content-between mt-2'>
                <Button type='button' color='primary' className='btn-prev' onClick={() => stepper.previous()}>
                    <ArrowLeft size={14} className='align-middle me-sm-25 me-0'></ArrowLeft>
                    <span className='align-middle d-sm-inline-block d-none'>Previous</span>
                </Button>
                <Button.Ripple type="submit" color="primary" tag={Link} to='/settings/plan2'>
                    Done
                </Button.Ripple>
            </div>
        </Card>
    )
}

export default Lisence
