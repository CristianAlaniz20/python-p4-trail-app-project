import React from "react";
import Trail from "./Trail";

function AllTrails({ trails }) {
    return (
        <div>
            {/* Iterate through trails list and create a Trail JSX for each */}
            {trails.length > 0 ? (
              trails.map(trail => {
                return (
                  <Trail 
                    key={trail.id}
                    id={trail.id}
                    name={trail.name} 
                    address={trail.address} 
                    length={trail.length}
                    description={trail.description}
                    profileImage={trail.image_url}
                />
                )
            })
            ) : (
              <h4>
                Sorry, no trails were found!
              </h4>
            )}
        </div>
    )
}

export default AllTrails