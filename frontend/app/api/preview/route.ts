const BACKEND_URL = "https://ai-data-report-generator-zr71.onrender.com";

export async function POST(request: Request) {
  const formData = await request.formData();

  const response = await fetch(`${BACKEND_URL}/preview`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  return Response.json(data, {
    status: response.status,
  });
}