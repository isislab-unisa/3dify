import { connectToMongoDB } from "@/lib/mongodb";
import User from "@/models/user";
import { revalidatePath } from "next/cache";

type Body = {
    email: string;
    imageId: string;
};

export async function POST(req: Request) {
    try {
        await connectToMongoDB();
        const user: Body = await req.json();

        const existingUser = await User.findOne({ email: user.email });
        if (!existingUser) {
            return Response.json({ message: 'user does not exist.' });
        }

        if (existingUser.imageIds.includes(user.imageId)) {
            return Response.json({ message: 'image id already exists.' });
        }

        await User.updateOne({ email: user.email }, { $push: { imageIds: [user.imageId] } });

        revalidatePath("/");
        return Response.json({ message: 'added image id to the user successfully.' });
    } catch (error) {
        console.error('error adding image id to the user', error);
        return Response.json({ message: 'error adding image id to the user.' });
    }
}