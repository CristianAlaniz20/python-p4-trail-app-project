import React, { useState, useContext } from "react";
import LogInForm from "../components/LogInForm";
import SignUpForm from "../components/SignUpForm";
import ResponseMessage from "../components/ResponseMessage";
import { ResponseMessageContext }from "../components/ResponseMessageProvider";
import Header from "../components/Header";

function LogIn({ onLogin }) {
    const [hasAccount, setHasAccount] = useState(true)
    const {message, statusCode} = useContext(ResponseMessageContext)

    // CSS styling
    const loginStyle = {
        textAlign: "center",
    }

    return (
        <div style={loginStyle}>
            <Header />
            {/* conditionally shows Login form or Signup form */}
            {hasAccount ? (
                <>
                    <LogInForm onLogin={onLogin} />
                    <br />
                    <p>Don't have an account?</p>
                    <button onClick={() => setHasAccount(false)}>Create An Account</button>
                </>
            ) : (
                <>
                    <SignUpForm />
                    <br />
                    <p>Already have an account?</p>
                    <button onClick={() => setHasAccount(true)}>Go to Log In</button>
                </>
            )}
            {/* conditionally shows guiding message for users */}
            {message && statusCode ? <ResponseMessage /> : null}
        </div>
    )
}

export default LogIn;