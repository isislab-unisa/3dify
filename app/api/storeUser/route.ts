import { connectToMongoDB } from "@/lib/mongodb";
import User from "@/models/user";
import { revalidatePath } from "next/cache";

type Body = {
    email: string;
    name: string;
    imageIds: string[];
};

export async function POST(req: Request) {
    try {
        await connectToMongoDB();
        const user: Body = await req.json();

        const existingUser = await User.findOne({ email: user.email });
        if (existingUser) {
            return Response.json({ message: 'user already exists.' });
        }

        const newUser = await User.create({
            name: user.name,
            email: user.email,
            imageIds: user.imageIds,
        });
        newUser.save();

        revalidatePath("/");
        return Response.json({ message: 'user stored successfully.' });
    } catch (error) {
        console.log(error);
        return Response.json({ message: 'error storing user.' });
    }
}