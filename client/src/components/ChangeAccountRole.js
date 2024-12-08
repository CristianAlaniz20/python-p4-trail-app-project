import React from "react";
import { useFormik } from "formik"
import * as yup from "yup"

function ChangeAccountRole() {
    const formSchema = yup.object().shape({
        adminSecretKey: yup.string().required("Must enter admind secret key.")
    })

    const formik = useFormik({
        initialValues : {
            adminSecretKey: ""
        },
        validationSchema: formSchema,
        onSubmit: (values) => {
            fetch("/user", {
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
        }
    })

    return (
        <div>
            <h2>Change Account Role Form</h2>
            <form onSubmit={formik.handleSubmit} >
                <label htmlFor="adminSecretKey">Enter Admin Secret Key:</label>
                <input 
                    id="adminSecretKey"
                    name="adminSecretKey"
                    
                />
                <br />
        
                <button type="submit" >Submit Key</button>
            </form>
        </div>
    )
}

export default ChangeAccountRole