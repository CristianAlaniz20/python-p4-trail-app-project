import React, { useContext } from "react";
import { useFormik } from "formik";
import * as yup from "yup";
import { ResponseMessageContext } from "./ResponseMessageProvider";

function UpdateUser({ user, setUser, setUpdateUser, userPassword }) {
    const { handleResponse } = useContext(ResponseMessageContext)

    // verification for the form inputs
    const formSchema = yup.object().shape({
        newUsername: yup.string(),
        newPassword: yup.string(),
        newProfileImage: yup.string(),
        newBio: yup.string()
    })

    // Use formik to handle form
    const formik = useFormik({
        initialValues : {
            newUsername: user.username || "",
            newPassword: userPassword || "",
            newProfileImage: user.profile_image_url || "",
            newBio: user.bio || ""
        },
        validationSchema: formSchema,
        onSubmit: (values) => {
            // PUT request to EditUser resource
            fetch("/edit_user", {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(values, null, 2),
            })
            .then((res) => handleResponse(res, () => setUpdateUser(false)))
            .then(resUser => setUser(resUser))
            .catch(error => console.error(error))
          },
        })

    return (
        <div>
            <h2>Update Account Form</h2>
            <p>If you do not wish to update a field, leave it alone. System will automatically use the old value for the respective fields.</p>
            <form onSubmit={formik.handleSubmit} >
                <label htmlFor='newUsername'>New Username: </label>
                <input
                id='newUsername' 
                name='newUsername'
                onChange={formik.handleChange}
                value={formik.values.newUsername}
                />
                <br />

                <label htmlFor='newPassword'>New Password: </label>
                <input
                id='newPassword'
                name='newPassword'
                type="password"
                onChange={formik.handleChange}
                value={formik.values.newPassword}
                />
                <br />

                <label htmlFor='newProfileImage'>New Profile Image URL: </label>
                <input
                id='newProfileImage'
                name='newProfileImage' 
                onChange={formik.handleChange}
                value={formik.values.newProfileImage}
                />
                <br />

                <label htmlFor='newBio'>New Bio: </label>
                <input
                id='newBio'
                name='newBio'
                onChange={formik.handleChange}
                value={formik.values.newBio}
                />
                <br />

                <button type="submit">Update Account</button>
            </form>
        </div>
    )
}

export default UpdateUser