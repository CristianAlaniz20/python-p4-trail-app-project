import React, { useContext } from "react";
import { useFormik } from "formik";
import * as yup from "yup";
import { ResponseMessageContext } from "./ResponseMessageProvider";

function SignUpForm() {
    const { handleResponse } = useContext(ResponseMessageContext)

    // formik validation schema
    const formSchema = yup.object().shape({
        username: yup.string().required("Must enter a username."),
        password: yup.string().required("Must enter a password")
    })

    const formik = useFormik({
        initialValues : {
            username: "",
            password: "",
            profileImage: "",
            bio: ""
        },
        validationSchema: formSchema,
        onSubmit: (values) => {
            // POST request to Signup Resource
            fetch("/signup", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(values, null, 2),
            })
            .then((res) => handleResponse(res))
            .catch(error => console.error(error))
          },
        })
    
    return (
        <>
            <h2>User Sign Up Form</h2>
            <form onSubmit={formik.handleSubmit}>
                <label htmlFor='username'>Username: </label>
                <input
                id='username' 
                name='username'
                type="text"
                onChange={formik.handleChange}
                value={formik.values.username}
                />
                <br />

                <label htmlFor='password'>Password: </label>
                <input
                id='password'
                name='password'
                type="password"
                onChange={formik.handleChange}
                value={formik.values.password}
                />
                <br />

                <label htmlFor='profileImage'>Profile Image URL: </label>
                <input
                id='profileImage'
                name='profileImage'
                type="text" 
                onChange={formik.handleChange}
                value={formik.values.profileImage}
                />
                <br />

                <label htmlFor='bio'>Bio: </label>
                <input
                id='bio'
                name='bio'
                type="text"
                onChange={formik.handleChange}
                value={formik.values.bio}
                />
                <br />

                <button type="submit">Sign Up</button>
        </form>
      </>
    )
}

export default SignUpForm