//To execute (from root folder) : npm test

const { GetGenderAndAgeFromPhoto } = require('../internal/scanface');
const fs = require('fs');
const path = require('path');
const faceapi = require("face-api.js");
const canvas = require("canvas");
const { afterEach } = require('node:test');

jest.mock('face-api.js');
jest.mock('canvas');

beforeEach(() => {
    jest.spyOn(console, "warn").mockImplementation(() => {});
});

// afterEach(() => {
//     console.warn.mockRestore();
// });

test("GenderAndAgeFromPhoto", async () => {
    const filePath = path.join(__dirname, 'test_file/correctImage.txt');
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    const result = await GetGenderAndAgeFromPhoto(fileContent, 500);
    expect(result).toHaveProperty("age");
    expect(result).toHaveProperty("gender");
    expect(result.age).toBeGreaterThan(0);
});

test("GenderAndAgeFromPhotoWrong", async () => {
    const filePath = path.join(__dirname, 'test_file/wrongImage.txt');
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    await expect(GetGenderAndAgeFromPhoto(fileContent, 500)).rejects.toThrow();
});

test("GenderAndAgeFromPhotoNoFace", async () => {
    const filePath = path.join(__dirname, 'test_file/noFace.txt');
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    await expect(GetGenderAndAgeFromPhoto(fileContent, 500)).rejects.toThrow();
});

