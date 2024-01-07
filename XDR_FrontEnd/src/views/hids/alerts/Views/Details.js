// ================================================================================================
//  File Name:  Details.js
//  Description: Details of the Col Details.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Fragment } from 'react'
import { Card, Row, Col, Badge } from 'reactstrap'

const Details = ({agent_details}) => {
console.log(agent_details)

    return (
        <Fragment>
            <Card>
                <div className='ml-1 mt-1 mb-1'>
            <Row>
                  <Col xs={1} md={1}> ID
                  <br/>
                  <Badge color='primary'>{agent_details.agent_id}</Badge>
                  </Col>
                  <Col md={0.5} xs={0}></Col>
                  <Col xs={1} md={1}> Status
                  <br/>
                  <Badge color='primary'>active</Badge>
                  </Col>
                  <Col md={1} xs={1}></Col>
                  <Col xs={1} md={1}> IP
                  <br/>
                  <Badge color='primary'>10.1.0.34</Badge>
                  </Col>
                  <Col md={1} xs={1}></Col>
                  <Col xs={1} md={1}> Version
                  <br/>
                  <Badge color='primary'>Wazuh v4.3.10</Badge>
                  </Col>
                  <Col md={1} xs={1}></Col>
                  <Col xs={1} md={1}> Groups
                  <br/>
                  <Badge color='primary'>default</Badge>
                  </Col>
                  <Col md={1} xs={1}></Col>
                  <Col xs={1} md={1}> Operating System
                  <br/>
                  <Badge color='primary'>Debian GNU/Linux 11</Badge>
                  </Col>
                  <Col md={1} xs={1}></Col>
                  <Col xs={1} md={1}> Cluster node
                  <br/>
                  <Badge color='primary'>node01</Badge>
                  </Col>
                </Row>
                </div>
            </Card>
        </Fragment>
    )
}

export default Details