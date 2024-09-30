import mongoose, { Document, Model } from 'mongoose';

export interface IUser extends Document {
    email: string;
    name: string;
    imageIds: string[];
}

const UserSchema = new mongoose.Schema<IUser>({
    email: {
        type: String,
        required: [true, 'Please provide an email for this user.'],
        unique: true,
    },
    name: {
        type: String,
        required: [true, 'Please provide a name for this user.'],
    },
    imageIds: {
        type: [String],
        default: [],
    },
});

const User: Model<IUser> = mongoose.models.User || mongoose.model<IUser>('User', UserSchema);

export default User;