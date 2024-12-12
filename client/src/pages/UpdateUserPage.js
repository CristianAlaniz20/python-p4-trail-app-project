import React, { useState } from "react";
import UpdateUser from "../components/UpdateUser";
import PasswordConfirmation from "../components/PasswordConfirmation";

function UpdateUserPage({ user, setUpdateUser }) {
    const [passwordConfirmed, setPasswordConfirmed] = useState(false)

    return (
        <>
            <h2>Update User Page</h2>
            {passwordConfirmed ? 
                <UpdateUser user={user} setUpdateUser={setUpdateUser} /> :
                <PasswordConfirmation user={user} setPasswordConfirmed={setPasswordConfirmed} />
            }
        </>
    )
}

export default UpdateUserPage