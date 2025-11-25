// Código vulnerable para la demo de Semgrep
const express = require("express");
const app = express();
const mysql = require("mysql");

// API Key hardcodeada (Semgrep lo detecta)
const API_KEY = "12345-FAKE-KEY-DO-NOT-USE";

app.get("/search", (req, res) => {
    const userInput = req.query.q;

    // Inyección SQL: concatenar strings en queries 
    const query = "SELECT * FROM users WHERE name = '" + userInput + "'";

    const connection = mysql.createConnection({
        host: "localhost",
        user: "root",
        password: "",
        database: "demo"
    });

    connection.query(query, (err, results) => {
        if (err) return res.send("Error en consulta");

        // XSS: devolver input del usuario sin sanitizar
        res.send("Resultados para: " + userInput);
    });
});

app.listen(3000, () => console.log("Servidor inseguro corriendo en puerto 3000"));