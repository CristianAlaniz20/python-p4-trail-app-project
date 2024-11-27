import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom/cjs/react-router-dom.min";
import Review from "../components/Review"
import Trail from "../components/Trail"

function TrailPage() {
    const [reviews, setReviews] = useState([])
    const [trail, setTrail] = useState({})
    const { trail_id } = useParams()

    useEffect(() => {
        // GET request for reviews with a trail_id equal to trail_id
        fetch(`/reviews/${trail_id}`)
        .then(res => {
            if (res.status === 200) {
              res.json()
              .then(resReviews => {
                console.log(`resReview: ${resReviews}`)
                setReviews(resReviews)
              })
            }
          })
        .catch(error => console.error(error))
    }, [reviews])

    useEffect(() => {
        // GET request for a trail with an id of trail_id
        fetch(`/trail/${trail_id}`)
        .then(res => {
            if (res.status === 200) {
              res.json()
              .then(resTrail => {
                console.log(`resTrail: ${resTrail}`)
                setTrail(resTrail)
              })
            }
          })
        .catch(error => console.error(error))
    }, [])

    return (
        <>
            <Trail 
                name={trail.name} 
                address={trail.address} 
                length={trail.length}
                description={trail.description}
                profileImage={trail.profileImage}
            />
            {/* Iterate through reviews list and create a Review JSX for each */}
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