const http = require("http");

let counter = 0;

// on each request, the server should increment a counter and return the current value of the counter in the response
// the server should return the counter value as JSON
const server = http.createServer((req, res) => {
    // increment by 1 on each request
    counter += 1;

    const currentDateTime = new Date();
    const data = {
        counter: counter.toString(),
        date: currentDateTime,
    };
    const jsonData = JSON.stringify(data);

    res.statusCode = 200;
    res.setHeader("Content-Type", "application/json");
    res.end(jsonData);
});

server.listen(3000, () => {
    console.log("Server running on port 3000");
    // log the current value of the counter to the console every 5 seconds
    setInterval(() => {
        console.log(counter);
    }, 5000);
});
