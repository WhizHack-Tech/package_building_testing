// ================================================================================================
//  File Name: index.js
//  Description: Details of the Soar Pages.
//  ----------------------------------------------------------------------------------------------
//  Item Name: Whizhack Client Dashboard
//  Author URL: https://whizhack.in
// ==============================================================================================
import { Spinner } from "reactstrap"
import { useSelector } from "react-redux"
import NotAuthorizedInner from '@src/views/notAuthorizedInner'
// import IframeMap from "./iframeMap"
import Maintenance from "./infoSoar"

export default () => {
    const pagePermissionStore = useSelector((store) => store.pagesPermissions)

    if (pagePermissionStore.loading === false) {
        return (
            <div className="text-center mt-5 pt-5"><Spinner md={5} color="primary" /></div>
        )
    } else {
        if (pagePermissionStore.env_soar === false) {
            return <NotAuthorizedInner />
        }
    }

    return <Maintenance />
}
