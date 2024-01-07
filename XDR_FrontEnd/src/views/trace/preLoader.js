// ================================================================================================
//  File Name: perLoader.js
//  Description: Details of the Trace ( Loader ).
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Spinner } from "reactstrap"
import '@styles/react/libs/tables/react-dataTable-component.scss'
import loaderSrc from "@assets/images/logo/nids.gif"

const styles = {
    loadingBox: {
        position: 'absolute',
        width: '100%',
        height: '100%',
        backgroundColor: '#0000002b',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center'
    },
    spinner: {
        backgroundColor: 'white',
        outline: "5px solid white"
    }
}

const PreLoader = () => {
    return <div style={styles.loadingBox} className="rounded">
        <img className='' style={{
            height: '50px',
            width: '50px'
        }} src={loaderSrc} alt='logo' />
        {/* <Spinner animation="border" color="primary" role="status" style={styles.spinner}>
        </Spinner> */}
    </div>
}

export default PreLoader