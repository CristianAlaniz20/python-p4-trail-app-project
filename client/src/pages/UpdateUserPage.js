import React, { useState } from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
import UpdateUser from "../components/UpdateUser";
import PasswordConfirmation from "../components/PasswordConfirmation";

function UpdateUserPage({ user }) {
    const [passwordConfirmed, setPasswordConfirmed] = useState(false)
    const [successfullyUpdated, setSuccessfullyUpated] = useState(false)
    const history = useHistory()

    if (successfullyUpdated) {
        history.push(`/user`)
    }

    return (
        <>
            <h2>Update User Page</h2>
            {passwordConfirmed ? 
                <UpdateUser user={user} setSuccessfullyUpated={setSuccessfullyUpated} /> :
                <PasswordConfirmation user={user} setPasswordConfirmed={setPasswordConfirmed} />
            }
        </>
    )
}

export default UpdateUserPage