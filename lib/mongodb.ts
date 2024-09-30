// importing mongoose library along with Connection type from it
import mongoose, { Connection } from "mongoose";

// declaring a variable to store the cached database connection
let cachedConnection: Connection | null = null;

// Function to establish a connection to MongoDB
export async function connectToMongoDB() {
    // if a cached connection exists, return it
    if (cachedConnection) {
        console.log("using cached db connection");
        return cachedConnection;
    }

    try {
        // if no cached connection exists, establish a new connection to MongoDB
        const cnx = await mongoose.connect(process.env.MONGODB_URI!);
        // cache the connection for future use
        cachedConnection = cnx.connection;
        // log message indicating a new MongoDB connection is established
        console.log("new mongodb connection established");
        // return the newly established connection
        return cachedConnection;
    } catch (error) {
        // if an error occurs during connection, log the error and throw it
        console.error(error);
        throw error;
    }
}