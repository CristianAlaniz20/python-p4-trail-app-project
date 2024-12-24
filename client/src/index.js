import React from "react";
import App from "./components/App";
import "./index.css";
import { createRoot } from "react-dom/client";
import ResponseMessageProvider from "./components/ResponseMessageProvider";

const container = document.getElementById("root");
const root = createRoot(container);
root.render(
    <ResponseMessageProvider>
        <App />
    </ResponseMessageProvider>
);
