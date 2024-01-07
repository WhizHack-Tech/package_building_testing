// ================================================================================================
//  File Name: expandableTableViews.js
//  Description: Details of the Dynamic Report.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
// ** Custom Components
import { Fragment, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Badge, Row, TabContent, TabPane, Nav, NavItem, NavLink, Col } from 'reactstrap'

// ** Expandable table component
const ExpandableTable = ({ data }) => {
    const { t } = useTranslation()
    const [active, setActive] = useState('1')
    const ObjKeys = Object.keys(data)
    const ObjVal = Object.values(data)

    const ListTableData = () => {

        if (ObjKeys.length > 0) {
            return ObjKeys.map((values, i) => {
                return (
                    <Row className="m-1" key={i}>
                        <Badge color='light-primary'>
                            <Col xs={4} md={4}>{values}</Col>
                        </Badge>
                        &nbsp;&nbsp;:
                        <Col xs={8} md={4}>{JSON.stringify(ObjVal[i])}</Col>
                    </Row>
                )
            })

        } else {
            return <p>{t('Data Not Found')}</p>
        }

    }

    const JsonRenderData = () => {

        if (ObjKeys.length > 0) {
            return <pre style={{ color: "#8177f2" }}> {JSON.stringify(data, null, '\t')} </pre>
        } else {
            return <p>{t('Data Not Found')}</p>
        }
    }

    const toggle = tab => {
        if (active !== tab) {
            setActive(tab)
        }
    }

    return (

        <Fragment>
            <div className='expandable-content'>
                <Nav tabs>
                    <NavItem>
                        <NavLink
                            active={active === '1'}
                            onClick={() => {
                                toggle('1')
                            }}
                        >
                            {t('Table')}
                        </NavLink>
                    </NavItem>
                    <NavItem>
                        <NavLink
                            active={active === '2'}
                            onClick={() => {
                                toggle('2')
                            }}
                        >
                            {t('JSON')}
                        </NavLink>
                    </NavItem>
                </Nav>
                <TabContent className='py-50 ml-1' activeTab={active}>
                    <TabPane tabId='1'>
                        <ListTableData />
                    </TabPane>
                    <TabPane tabId='2'>
                        <JsonRenderData />
                    </TabPane>
                </TabContent>
            </div>
        </Fragment>
    )
}

export default ExpandableTable
