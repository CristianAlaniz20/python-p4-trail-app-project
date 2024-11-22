import React, { useEffect, useState } from "react";
import Trail from "./Trail"

function AllTrails({ trails }) {
    const [trails, setTrails] = useState([])

    useEffect(() => {
        // get trails
        fetch("/trails")
        .then(res => {
          if (res.status === 200) {
            res.json()
            .then(resTrails => setTrails(resTrails))
          }
        })
        .catch(error => console.error(error))
      }, [])

    return (
        <div>
            {/* Iterate through trails list and create a Trail JSX for each */}
            {trails.forEach(trail => {
                <Trail 
                    name={trail.name} 
                    address={trail.address} 
                    length={trail.length}
                    description={trail.description}
                    profileImage={trail.image_url}
                />
            })
            }
        </div>
    )
}

export default AllTrails