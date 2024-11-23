import React, { useEffect, useState } from "react";
import Trail from "./Trail"

function AllTrails() {
    const [trails, setTrails] = useState([])

    useEffect(() => {
        // get trails
        console.log("About to fetch trails...")
        fetch("/trails")
        .then(res => {
          if (res.status === 200) {
            res.json()
            .then(resTrails => {
              console.log(`resTrail: ${resTrails}`)
              setTrails(resTrails)
            })
          }
        })
        .catch(error => console.error(error))
      }, [])

    return (
        <div>
            {/* Iterate through trails list and create a Trail JSX for each */}
            {trails.forEach(trail => {
                <Trail 
                    key={trail.id}
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