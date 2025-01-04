import React, { useContext } from "react";
import { ResponseMessageContext } from "../components/ResponseMessageProvider";

function DeleteUserPage({ setDeleteAccount, setUser }) {
    const { handleResponse } = useContext(ResponseMessageContext)

    // handle YES button click
    function handleYesClick() {
        fetch("/edit_user", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
              },
        })
        .then(res => handleResponse(res, () => setUser(null)))
        .catch(error => console.error(error))
    }

    // handle NO button click
    const handleNoClick = () => setDeleteAccount(false)

    // CSS styling 
    const deleteUserPageStyle = {
        textAlign: "center",
    }

    return (
        <div style={deleteUserPageStyle} >
            <p>
                All account information will be lost.
                Are you sure you want to delete your account?
            </p>
            <button onClick={handleYesClick} >YES</button>
            <button onClick={handleNoClick} >NO</button>
        </div>
    )
}

export default DeleteUserPage