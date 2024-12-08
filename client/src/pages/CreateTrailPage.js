import React from "react";
import { useFormik } from "formik";
import * as yup from "yup";

function CreateTrailPage() {
    // frontend validation for form
    const formSchema = yup.object().shape({
        trailName: yup.string().required("Must have a name."),
        trailAddress: yup.string().required("Must have full address."),
        trailLength: yup.string().required("Must enter trail length."),
        trailDescription: yup.string().required("Must have a description.").max(100, "Cannot have 100 or more characters."),
        trailImageUrl: yup.string().required("Must have an image url")
    })

    const formik = useFormik({
        initialValues: {
            trailName: "",
            trailAddress: "",
            trailLength: "",
            trailDescription: "",
            trailImageUrl: ""
        },
        validationSchema: formSchema,
        onSubmit: (values) => {
            // POST request to create trail resource
            fetch("/create_trail", {
                method: "POST", 
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(values, null, 2),
            })
            .then(res => {
                if (res.status === 201) {
                    console.log("Trail succesfully created")
                }
            })
            .catch(error => console.error(error))
        }
    })
    
    return (
        <div>
            <h2>Create Trail Page Form</h2>
            <form onSubmit={formik.handleSubmit}>
                <label htmlFor="trailName" >Trail Name:</label>
                <input 
                    id="trailName"
                    name="trailName"
                    type="text"
                    onChange={formik.handleChange}
                    value={formik.values.trailName}
                />
                <br />

                <label htmlFor="trailAddress" >Trail Address:</label>
                <input 
                    id="trailAddress"
                    name="trailAddress"
                    type="text"
                    onChange={formik.handleChange}
                    value={formik.values.trailAddress}
                />
                <br />

                <label htmlFor="trailLength" >Trail Length:</label>
                <input 
                    id="trailLength"
                    name="trailLength"
                    type="text"
                    onChange={formik.handleChange}
                    value={formik.values.trailLength}
                />
                <br />

                <label htmlFor="trailDescription" >Trail Description:</label>
                <input 
                    id="trailDescription"
                    name="trailDescription"
                    type="text"
                    onChange={formik.handleChange}
                    value={formik.values.trailDescription}
                />
                <br />

                <label htmlFor="trailImageUrl" >Trail Image URL</label>
                <input 
                    id="trailImageUrl"
                    name="trailImageUrl"
                    type="text"
                    onChange={formik.handleChange}
                    value={formik.values.trailImageUrl}
                />
                <button type="submit">Create Trail</button>
            </form>
        </div>
    )
}

export default CreateTrailPage