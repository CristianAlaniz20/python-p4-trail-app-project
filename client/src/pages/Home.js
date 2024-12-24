import React, { useState, useContext } from "react";
import { useFormik } from "formik";
import * as yup from "yup";
import AllTrails from "../components/AllTrails";
import { ResponseMessageContext } from "../components/ResponseMessageProvider";

function Home() {
    const [trails, setTrails] = useState([])
    const [hasSearched, setHasSearched] = useState(false)
    const { handleResponse } = useContext(ResponseMessageContext)

    const formSchema = yup.object().shape({
      city: yup.string().required("must enter a city!")
    })

    const formik = useFormik({
      initialValues : {
          city: ""
      },
      validationSchema: formSchema,
      onSubmit: (values) => {
          // POST request to get back trails with an adress of city
          fetch("trails_index", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(values, null, 2),
          })
          .then(res => handleResponse(res, () => setHasSearched(true)))
          .then(result => setTrails(result))
          .catch(error => console.error(error))
        },
    })

    return (
        <>
            <p>Disclaimer: If what you entered matches an address, it will be included in the result.</p>
            <form onSubmit={formik.handleSubmit}>
                <label htmlFor="city" >Enter City Here: </label>
                <input 
                  id="city"
                  name="city"
                  onChange={formik.handleChange}
                  value={formik.values.city}
                />
                <button type="submit">Search</button>
            </form>
            {hasSearched ? (
                <AllTrails trails={trails} />
            ) : (
                <h4>Trails awaits you...</h4>
            )}
        </>
    )
}

export default Home