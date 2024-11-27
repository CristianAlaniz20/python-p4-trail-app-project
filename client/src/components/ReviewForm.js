import React from "react";
import { useParams } from "react-router-dom/cjs/react-router-dom.min";
import { useFormik } from "formik";
import Header from "./Header";

function ReviewForm() {
    const { trail_id } = useParams()

    const formik = useFormik({
        initialValues: {
            rating: "",
            text: ""
        },
        onSubmit: (values) => {
            console.log(values)
            fetch(`reviews/${trail_id}`, {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify(values, null, 2),
            })
            .then((res) => {
                if (res.status === 201) {
                  console.log("Review Successfully created!")
                }
            })
            .catch(error => console.error(error))
            },
    })

    return (
        <>
            <Header />
            <h2>Create A Review Form:</h2>
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
        </>
    )
}

export default ReviewForm