import React, { useState } from "react";
import { useFormik } from "formik";
import AllTrails from "../components/AllTrails";

function Home() {
    const [trails, setTrails] = useState([])
    const [hasSearched, setHasSearched] = useState(false)

    const formik = useFormik({
      initialValues : {
          city: ""
      },
      onSubmit: (values) => {
          // POST request to get back trails with an adress of city
          fetch("trails_index", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(values, null, 2),
          })
          .then(res => {
            if (res.status === 201) {
              res.json()
              .then(resTrails => {
                setTrails(resTrails)
                setHasSearched(true)
              })
            }
          })
          .catch(error => console.error(error))
        },
    })

    return (
        <>
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