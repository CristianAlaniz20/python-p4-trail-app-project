import React from "react";

function Review({ rating, text, username }) {
    return (
        <div className="reviews" >
            <h3 className="review-usernames" >{username}</h3>
            <p className="review-text" >{text}</p>
            <p className="review-rating" >{rating} out of 5</p>
        </div>
    )
}

export default Review