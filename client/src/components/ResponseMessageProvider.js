import React, { createContext, useState } from 'react';

// Create the context
export const ResponseMessageContext = createContext()

function ResponseMessageProvider({ children }) {
    // declare states
    const [message, setMessage] = useState(null)
    const [statusCode, setStatusCode] = useState(null)
    const [isSubmitted, setIsSubmitted] = useState(false)

    // function to handle all fetch request responses
    async function handleResponse(response, ...callbacks) {
        setStatusCode(response.status)
        const data = await response.json()
        let result;

        if (response.ok) {
            setMessage(data.message)
            // if the callbacks list is NOT empty: for each callback in callbacks, run the callback function
            if (callbacks.length > 0) {
                callbacks.forEach(callback => callback())
            }
            // if response contains expected_data: set it to result
            if (data.expected_data) {
                result = data.expected_data
            }
        } else {
            setMessage(data.error)
        }

        setIsSubmitted(true)
        return result
    }

    return (
        <ResponseMessageContext.Provider value={{message, statusCode, isSubmitted, setIsSubmitted, handleResponse}} >
            {children}
        </ResponseMessageContext.Provider>
    )
}

export default ResponseMessageProvider