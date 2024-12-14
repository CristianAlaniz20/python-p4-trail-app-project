import React from "react";

function DeleteUserPage({ setDeleteAccount, setUser }) {
    // handle YES button click
    function handleYesClick() {
        fetch("/edit_user", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
              },
        })
        .then(res => {
            if (res.status == 204) {
                console.log("Successfully deleted account!")
                setUser(null)
            }
        })
        .catch(error => console.error(error))
    }

    // handle NO button click
    const handleNoClick = () => setDeleteAccount(false)

    return (
        <div>
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