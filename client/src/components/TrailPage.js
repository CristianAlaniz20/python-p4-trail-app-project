import React, { useState, useEffect } from "react";
import Review from "./Review"
import Trail from "./Trail"

function TrailPage({ name, address, length, description, profileImage }) {
    const [reviews, setReviews] = useState([])

    useEffect(() => {
        fetch("/reviews", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ "id" : id }),
        })
        .then(res => {
            if (res.status === 201) {
              res.json()
              .then(resReviews => {
                console.log(`resReview: ${resReviews}`)
                setReviews(resReviews)
              })
            }
          })
        .catch(error => console.error(error))
    }, [reviews])

    return (
        <>
            <Trail 
                name={name} 
                address={address} 
                length={length}
                description={description}
                profileImage={profileImage}
            />
            {reviews.length > 0 ? (
                reviews.map(review => {
                    return (
                        <Review 
                            key={review.id}
                            rating={review.rating}
                            text={review.text}
                            username={review._username}
                        />
                    )
                })
            ) : (
                <h4>This trail has no reviews.</h4>
            ) }
        </>
    )

}

export default TrailPage