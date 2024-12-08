import React from "react";
import { useFormik } from "formik"
import * as yup from "yup"

function ChangeAccountRole({ setShowChangeAccRole }) {
    // Validation for input
    const formSchema = yup.object().shape({
        adminSecretKey: yup.string().required("Must enter admind secret key.")
    })

    const formik = useFormik({
        initialValues : {
            adminSecretKey: ""
        },
        validationSchema: formSchema,
        onSubmit: (values) => {
            console.log(values)
            // POST request to change user role 
            fetch("/change_user_role", {
                method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(values, null, 2),
            })
            .then(res => {
                if (res.status === 201) {
                    console.log("Successfully changed role")
                }
            })
            .catch(error => console.error(error))
        },
    })

    // handle Back to User Information button click
    function handleBackToUserInfoClick() {
        console.log("Back  to User Info button pressed!")
        setShowChangeAccRole(false)
    }

    return (
        <div>
            <h2>Change Account Role Form</h2>
            <form onSubmit={formik.handleSubmit} >
                <label htmlFor="adminSecretKey">Enter Admin Secret Key:</label>
                <input 
                    id="adminSecretKey"
                    name="adminSecretKey"
                    type="password"
                    onChange={formik.handleChange}
                    value={formik.values.adminSecretKey}
                />
                <br />
        
                <button type="submit" >Submit Key</button>
            </form>
            <br />

            <button onClick={handleBackToUserInfoClick} >Back to User Information</button>
        </div>
    )
}

export default ChangeAccountRole