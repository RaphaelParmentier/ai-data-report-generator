const BACKEND_URL = "https://ai-data-report-generator-zn71.onrender.com";

export async function POST(request: Request) {
  try {
    const formData = await request.formData();

    const response = await fetch(`${BACKEND_URL}/sheets`, {
      method: "POST",
      body: formData,
    });

    const contentType = response.headers.get("content-type");

    if (!contentType?.includes("application/json")) {
      const text = await response.text();

      return Response.json(
        {
          detail:
            text || "Backend returned a non-JSON response while listing sheets.",
        },
        { status: response.status }
      );
    }

    const data = await response.json();

    return Response.json(data, {
      status: response.status,
    });
  } catch (error) {
    return Response.json(
      {
        detail:
          error instanceof Error
            ? error.message
            : "Unknown error while calling sheets API.",
      },
      { status: 500 }
    );
  }
}