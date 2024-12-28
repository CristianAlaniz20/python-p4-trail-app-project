import React, { useContext } from "react";
import { useFormik } from "formik";
import * as yup from "yup";
import { ResponseMessageContext } from "./ResponseMessageProvider";

function PasswordConfirmation({ setPasswordConfirmed, setUserPassword }) {
    const { handleResponse } = useContext(ResponseMessageContext)

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
            // POST request to check password resource
            fetch("/check_password", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                  },
                  body: JSON.stringify(values, null, 2),
            })
            .then(res => handleResponse(res, () => setPasswordConfirmed(true), () => setUserPassword(formik.values.confirmationPassword)))
            .catch(error => console.error(error))
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
                    type="password"
                    onChange={formik.handleChange}
                    value={formik.values.confirmationPassword}
                />
                <br />

                <button type="submit" >Check Password</button>
            </form>
        </div>
    )
}

export default PasswordConfirmation