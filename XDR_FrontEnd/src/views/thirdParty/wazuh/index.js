import { useSelector } from "react-redux"
import { Redirect } from "react-router-dom"
import { Spinner } from 'reactstrap'
import Components from "./components/"

const Wazuh = () => {
    const pagePermissionStore = useSelector((store) => store.pagesPermissions)

    if (pagePermissionStore.loading === false) {
        return (
            <div className="text-center mt-5 pt-5"><Spinner md={5} /></div>
        )
    } else {
        if (pagePermissionStore.env_wazuh === false) {
            return <Redirect to='/not-authorized' />
        }
    }

    return <Components />
}

export default Wazuh