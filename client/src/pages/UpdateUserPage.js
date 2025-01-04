import React, { useState } from "react";
import UpdateUser from "../components/UpdateUser";
import PasswordConfirmation from "../components/PasswordConfirmation";

function UpdateUserPage({ user, setUpdateUser }) {
    const [passwordConfirmed, setPasswordConfirmed] = useState(false)
    const [userPassword, setUserPassword] = useState("")

    const updateUserStyle = {
        textAlign: "center",
    }

    return (
        <div style={updateUserStyle} >
            <h2>Update User Page</h2>
            {passwordConfirmed ? 
                <UpdateUser user={user} setUpdateUser={setUpdateUser} userPassword={userPassword} /> :
                <PasswordConfirmation setPasswordConfirmed={setPasswordConfirmed} setUserPassword={setUserPassword} />
            }
        </div>
    )
}

export default UpdateUserPage