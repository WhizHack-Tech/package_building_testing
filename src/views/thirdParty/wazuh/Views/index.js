import { useSelector } from "react-redux"
import { Redirect } from "react-router-dom"
import { Spinner } from 'reactstrap'
import WazuhById from "./wazuhById"
const WazuhView = () => {
  //this section for page permission #START
  const pagePermissionStore = useSelector((store) => store.pagesPermissions)

  if (pagePermissionStore.loadding) {
    return (
      <div className="text-center mt-5 pt-5"><Spinner md={5} /></div>
    )
  } else {
    if (pagePermissionStore.env_View === false) {
      return <Redirect to='/not-authorized' />
    }
  }
  //this section for page permission #END

  return <WazuhById/>
}

export default WazuhView