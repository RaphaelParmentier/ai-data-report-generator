export async function postFormData<T>(
  endpoint: string,
  formData: FormData
): Promise<T> {
  const response = await fetch(`/api${endpoint}`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new Error(payload?.detail ?? "Erreur API inconnue.");
  }

  return response.json();
}