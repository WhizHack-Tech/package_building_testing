// ================================================================================================
//  File Name: preLoader.js
//  Description: Details of the Static Report loader Page.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Spinner } from "reactstrap"
import '@styles/react/libs/tables/react-dataTable-component.scss'

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
        <Spinner animation="border" color="primary" role="status" style={styles.spinner}>
        </Spinner>
    </div>
}

export default PreLoader