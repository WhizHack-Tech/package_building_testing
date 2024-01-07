import { Spinner } from "reactstrap"
import { useSelector } from "react-redux"
import NotAuthorizedInner from '@src/views/notAuthorizedInner'

export default () => {
    const pagePermissionStore = useSelector((store) => store.pagesPermissions)

    if (pagePermissionStore.loading === false) {
        return (
            <div className="text-center mt-5 pt-5"><Spinner md={5} color="primary" /></div>
        )
    } else {
        if (pagePermissionStore.env_tps === false) {
            return <NotAuthorizedInner />
        }
    }

    return <h1>TP Source</h1>
}