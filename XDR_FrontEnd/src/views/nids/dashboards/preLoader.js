import { Spinner } from "reactstrap"

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
        backgroundColor:'white',
        outline:"5px solid white"
    }
}

const PreLoader = () => {
    return <div style={styles.loadingBox} className="rounded">
        <Spinner animation="border" color="primary" role="status" style={styles.spinner}>
        </Spinner>
    </div>
}

export default PreLoader