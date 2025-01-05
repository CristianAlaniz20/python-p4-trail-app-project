import React, { useContext } from "react";
import { useParams, useHistory } from "react-router-dom/cjs/react-router-dom.min";
import { useFormik } from "formik";
import * as yup from "yup"
import { ResponseMessageContext } from "./ResponseMessageProvider";

function ReviewForm() {
    const { trail_id } = useParams()
    const history = useHistory()
    const { handleResponse } = useContext(ResponseMessageContext)

    // validation schema for formik
    const formSchema = yup.object().shape({
        rating: yup.string().required("Must enter a username."),
        text: yup.string().required("Must enter a password")
    })

    const formik = useFormik({
        initialValues: {
            rating: "",
            text: ""
        },
        validationSchema: formSchema,
        onSubmit: (values) => {
            // POST request to create new review
            fetch(`/reviews/${trail_id}`, {
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

    // Re routes to Trail Page
    const handleBackToTrailClick = () => history.push(`/trails/${trail_id}`)

    const reviewFormStyle = {
        textAlign: "center",
    }
    
    return (
        <div style={reviewFormStyle}>
            <h2>Create A Review Form</h2>
            <form onSubmit={formik.handleSubmit} >
                <label htmlFor="rating" >Rating: </label>
                <input 
                    id="rating"
                    name="rating"
                    onChange={formik.handleChange}
                    value={formik.values.rating}
                />
                <br />

                <label htmlFor="text" >Review:</label>
                <input 
                    id="text"
                    name="text"
                    onChange={formik.handleChange}
                    value={formik.values.text}
                />
                <br />

                <button type="submit" >Create Review</button>
            </form>
            <p>OR</p>
            <button onClick={handleBackToTrailClick}>Back to Trail</button>
        </div>
    )
}

export default ReviewForm