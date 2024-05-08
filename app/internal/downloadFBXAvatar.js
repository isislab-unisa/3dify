export async function sendJsonModifiers(makeHumanParameters) {
    let outputFile = JSON.stringify(makeHumanParameters)

    await saveJsonFile(outputFile)
}

async function saveJsonFile(text) {
    const res = await fetch('/applymodifiers', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text})
            });
    console.log(res)
}

export async function downloadFBX() {
    const options = {
        method: 'GET',
    };
    const res = await fetch('/downloadFbxZip', options)
    return res.blob();
  }