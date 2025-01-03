import React, { useState, useEffect, useContext } from "react";
import { ResponseMessageContext } from "./ResponseMessageProvider";

function ResponseMessage() {
    const [visible, setVisible] = useState(true)
    const { message, statusCode, isSubmitted, setIsSubmitted } = useContext(ResponseMessageContext)

    // Create a timer of 5 seconds where the response is visible for 5 seconds upon isSubmitted being clicked
    useEffect(() => {
        let timer;

        // if isSubmitted is true, set timer to setTimeout function
        if (isSubmitted) {
            setVisible(true)
            timer = setTimeout(() => {
                setVisible(false)
                setIsSubmitted(false)
            }, 5000)
        }

        // Cleanup the timer if the component unmounts before the timer completes
        return () => clearTimeout(timer)
    },[isSubmitted]);

    // if visible is false, return nothing
    if (!visible) return null;

    // condtionally sets the color of the response message
    const status = statusCode === 200 || statusCode === 201 || statusCode === 204 ? "green" : "red"

    // Response Message CSS styling
    const messageStyle = {
        backgroundColor: status,
        color: 'white',
        padding: '10px',
        margin: '10px 0',
    };

    return <div style={messageStyle} >{message}</div>
}

export default ResponseMessage