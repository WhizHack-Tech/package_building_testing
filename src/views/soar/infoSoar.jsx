// ================================================================================================
//  File Name: infoSoar.jsx
//  Description: Details of the Soar Pages.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { CardBody, Card } from "reactstrap"
import Logo from '@src/assets/images/logo/soar-logo.png'
import '@styles/base/pages/page-misc.scss'
import { useTranslation } from 'react-i18next'
import TableData from './TableData'
import Breadcrumbs from '@components/breadcrumbs/bread'
import { Fragment } from "react"
const _URL = "https://xdr-demo-response.zerohack.in"
const InfoSoar = () => {
    const {t} = useTranslation()

    return (
        <Fragment>
             <Breadcrumbs breadCrumbTitle='SOAR' />
        {/* <Card>
            <CardBody>
                <div className="misc-inner p-2">
                    <div className="w-100 text-center">
                        <a href={_URL} target='_blank'>
                            <img src={Logo} alt="logo" width="350" className="mb-3" />
                        </a>
                        <p className="mb-3">
                            {t('Kindly click on the button below to open SOAR in a new tab and login using the provided credentials')}
                        </p>
                        <a
                            className='mr-1 mb-1 btn btn-outline-primary'
                            color='primary'
                            href={_URL}
                            target='_blank'
                        >{t('Link')}</a>
                    </div>
                </div>
            </CardBody>
        </Card> */}
        <TableData />
        </Fragment>
    )
}
export default InfoSoar
