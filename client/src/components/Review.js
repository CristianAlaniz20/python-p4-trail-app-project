import React from "react";

function Review({ rating, text, username }) {
    const reviewStyle = {
        border: "1px solid",
    }

    return (
        <div className="reviews" style={reviewStyle} >
            <h3 className="review-usernames" >{username}</h3>
            <p className="review-text" >{text}</p>
            <p className="review-rating" >{rating} out of 5</p>
        </div>
    )
}

export default Review