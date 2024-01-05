import { useSelector } from "react-redux"
import { Redirect } from "react-router-dom"
import { Spinner } from 'reactstrap'
const Trace = () => {
    const pagePermissionStore = useSelector((store) => store.pagesPermissions)

    if (pagePermissionStore.loading === false) {
        return (
            <div className="text-center mt-5 pt-5"><Spinner md={5} /></div>
        )
    } else {
        if (pagePermissionStore.env_trace === false) {
            return <Redirect to='/not-authorized' />
        }
    }

    return <h1>Work Trace</h1>
}

export default Trace