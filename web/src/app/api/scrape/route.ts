import { NextRequest, NextResponse } from "next/server";
import { spawn } from "child_process";
import path from "node:path";

const ALLOW_ORIGIN = "*"; // dev only. Lock this down in prod.

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": ALLOW_ORIGIN,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
  };
}
export async function OPTIONS() {
  return new NextResponse(null, { status: 204, headers: corsHeaders() });
}

export async function POST(req: NextRequest) {
  try {
    const { url } = await req.json();
    if (!url) {
      return NextResponse.json({ error: "URL is required" }, { status: 400, headers: corsHeaders() });
    }

    const pythonExecutable = path.resolve(process.cwd(), "../backend/.venv/Scripts/python.exe");
    const cwd = path.resolve(process.cwd(), "../backend");

    // Buffer stdout so we can return the parsed job JSON to the caller
    const args = ["-m", "src.app", url];
    const python = spawn(pythonExecutable, args, { cwd });

    let stdout = "";
    let stderr = "";

    python.stdout.on("data", (d) => (stdout += d.toString()));
    python.stderr.on("data", (d) => (stderr += d.toString()));

    const exitCode: number = await new Promise((resolve) => {
      python.on("close", resolve);
    });

    if (exitCode !== 0) {
      console.error("Python stderr:", stderr);
      return NextResponse.json({ error: "Scrape failed", stderr }, { status: 500, headers: corsHeaders() });
    }

    // Your Python prints a JSON object of the job; try to parse it:
    let data: any = null;
    try { data = JSON.parse(stdout); } catch { /* might be logs preceding JSON */ }

    return NextResponse.json(
      data ?? { ok: true, raw: stdout },
      { status: 200, headers: corsHeaders() }
    );
  } catch (err: any) {
    return NextResponse.json({ error: err?.message ?? "Unknown error" }, { status: 500, headers: corsHeaders() });
  }
}