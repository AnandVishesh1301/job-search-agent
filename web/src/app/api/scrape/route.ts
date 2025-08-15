import { NextRequest, NextResponse } from "next/server";
import { spawn } from "child_process";
import path from "path";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { url } = body;

    if (!url) {
      return NextResponse.json({ error: "URL is required" }, { status: 400 });
    }

    // Path to the Python executable in the backend's venv
    const pythonExecutable = path.resolve(
      process.cwd(),
      "../backend/.venv/Scripts/python.exe"
    );
    // Path to the Python script
    const pythonScript = path.resolve(
      process.cwd(),
      "../backend/src/app.py"
    );

    console.log(`Executing: ${pythonExecutable} -m src.app ${url}`);

    const pythonProcess = spawn(pythonExecutable, ["-m", "src.app", url], {
      cwd: path.resolve(process.cwd(), "../backend"),
    });

    pythonProcess.stdout.on("data", (data) => {
      console.log(`stdout: ${data}`);
    });

    pythonProcess.stderr.on("data", (data) => {
      console.error(`stderr: ${data}`);
    });

    return NextResponse.json(
      { message: "Scraping process started. Check your terminal for output." },
      { status: 202 }
    );
  } catch (error) {
    console.error("Error in scrape endpoint:", error);
    return NextResponse.json(
      { error: "An internal server error occurred." },
      { status: 500 }
    );
  }
}
