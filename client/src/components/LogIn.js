import React, { useState } from "react";
import LogInForm from "./LogInForm";
import SignUpForm from "./SignUpForm";

function LogIn({ onLogin }) {
    const [hasAccount, setHasAccount] = useState(true)

    return (
        <div>
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
        </div>
    )
}

export default LogIn;