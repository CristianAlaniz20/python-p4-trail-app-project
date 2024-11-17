import React, { useState } from "react";
import LogInForm from "./LogInForm";
import SignUpForm from "./SignUpForm";

function LogIn() {
    const [hasAccount, setHasAccount] = useState(true)

    return (
        <div>
            {hasAccount ? (
                <>
                    <LogInForm />
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