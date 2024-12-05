import React from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";

function Trail({ id, name, address, length, description, profileImage }) {
    const history = useHistory()

    function handleTrailDivClick() {
        history.push(`/trails/${id}`)
    }

    function handleSaveTrailClick() {
        const trailIdObject = { id: id }
        fetch("/saved_trails", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(trailIdObject, null, 2),
        })
        .then(res => {
            if (res.status === 200 || res.status === 201) {
                res.json()
                .then(data => {
                    console.log(data)
                    console.log("Trail sucessfully saved!")
                })
            }
        })
        .catch(error => console.error(error))
    }

    return (
        <>
            <div onClick={handleTrailDivClick} >
                <img className="trail-pic" src={profileImage} alt={`${name} trail-pic`} />
                <h4 className="trail-name" >{name}</h4>
                <address className="trail-adress">{address}</address>
                <p className="trail-length" >{length} miles</p>
                <p className="trail-description" >{description}</p>
            </div>
            <button onClick={handleSaveTrailClick} >Save Trail</button>
        </>
    )
}

export default Trail