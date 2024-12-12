import React, { useState } from "react";
import { useFormik } from "formik";
import * as yup from "yup";

function PasswordConfirmation({ user, setPasswordConfirmed }) {
    // create a error message state
    const [errorMessage, setErrorMessage] = useState(null)
    
    // formik validation
    const formSchema = yup.object().shape({
        confirmationPassword: yup.string()
    })

    // using formik to handle form submission
    const formik = useFormik({
        initialValues: {
            confirmationPassword: ""
        },
        validationSchema: formSchema,
        onSubmit: (values) => {
            if (user.authenticate(values.confirmationPassword) === true) {
                setPasswordConfirmed(true)
            } 
            else {
                setErrorMessage("Invalid password please try again!")
            }
        }
    })

    return (
        <div>
            <h2>Password Authentication</h2>
            <p>
                Please enter your password for authentication purposes.
                Afterwards you will be redirected to update your account.
            </p>
            <form onSubmit={formik.handleSubmit} >
                <label>Enter Password: </label>
                <input 
                    id="confirmationPassword"
                    name="confirmationPassword"
                    onChange={formik.handleChange}
                    value={formik.values.confirmationPassword}
                />
                <br />

                <button type="submit" >Check Password</button>
            </form>

            {/* Print error message if the password is invalid */}
            {errorMessage ? (
                <p>{errorMessage}</p>
            ) : null}
        </div>
    )
}

export default PasswordConfirmation