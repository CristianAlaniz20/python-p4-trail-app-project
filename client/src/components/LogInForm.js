import React, { useState, useEffect } from "react";
import { useFormik } from "formik"
import * as yup from "yup"

function LogInForm() {
    const [trails, setTrails] = useState([{}]);
    const [refreshPage, setRefreshPage] = useState(false);

    useEffect(() => {
        console.log("FETCH! ");
        fetch("/trails")
        .then((res) => res.json())
        .then((data) => {
            setTrails(data);
            console.log(data);
        });
    }, [refreshPage]);

    const formSchema = yup.object().shape({
        username: yup.string().required("Must enter a username."),
        password: yup.string().required("Must enter a password")
    })

    const formik = useFormik({
        intialValues : {
            username: "",
            password: ""
        },
        validationSchema: formSchema,
        onSubmit: (values) => {
            fetch("trails", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(values, null, 2),
            })
            .then((res) => {
              if (res.status == 201) {
                setRefreshPage(!refreshPage)
              }
            })
          },
        })
        
    
    return (
        <>
            <h2>User Log In Form</h2>
            <form>
                <label htmlFor='username'>Username: </label>
                <input
                id='username' 
                name='username' 
                />
                <br />

                <label htmlFor='password'>Password: </label>
                <input
                id='password'
                name='password'
                />
                <br />

                <button>Log In</button>
            </form>
        </>
    )
}

export default LogInForm;