import React, { useState } from "react";
import { useFormik } from "formik";
import Trail from "./Trail";

function AllTrails() {
    const [trails, setTrails] = useState([])

    const formik = useFormik({
      initialValues : {
          city: ""
      },
      onSubmit: (values) => {
          fetch("trails", {
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
              })
            }
          })
          .catch(error => console.error(error))
        },
    })

    return (
        <div>
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
            {/* Iterate through trails list and create a Trail JSX for each */}
            {trails.length > 0 ? (
              trails.map(trail => {
                return (
                  <Trail 
                    key={trail.id}
                    name={trail.name} 
                    address={trail.address} 
                    length={trail.length}
                    description={trail.description}
                    profileImage={trail.image_url}
                />
                )
            })
            ) : (
              <h4>Trails awaits you...</h4>
            )}
        </div>
    )
}

export default AllTrails